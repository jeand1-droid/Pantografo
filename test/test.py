# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, Timer


@cocotb.test()
async def test_project(dut):

    # RELOJ DE 10 MHz
    clock = Clock(dut.clk, 100, unit="ns")
    cocotb.start_soon(clock.start())

    # CONFIGURACION
    TIMEOUT = 1000000
    PERIODO_NS = 100

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    # FUNCION DE ESPERA
    async def esperar(ciclos):
        await ClockCycles(dut.clk, ciclos)
        await FallingEdge(dut.clk)

    # FUNCION DE REINICIO
    async def reiniciar():
        await FallingEdge(dut.clk)

        dut.rst_n.value = 0
        dut.ui_in.value = 0

        await esperar(10)

        dut.rst_n.value = 1

        await esperar(5)

    # FUNCION PARA VERIFICAR SALIDAS
    def verificar(esperado):
        obtenido = int(dut.uo_out.value)

        assert obtenido == esperado, (
            f"Esperado: {esperado:08b}, "
            f"Obtenido: {obtenido:08b}"
        )

    # PRUEBA 1: REPOSO

    await reiniciar()

    dut._log.info("PRUEBA 1: Reposo")

    verificar(0b00000000)

    # PRUEBA 2: MOVIMIENTO NORMAL X-Y

    await reiniciar()

    dut._log.info("PRUEBA 2: Movimiento normal")

    for i in range(20):

        dut.ui_in.value = 0b00001111
        await esperar(5)

        dut.ui_in.value = 0b00000011
        await esperar(5)

        verificar(0b00000000)

    # PRUEBA 3: LIMITE X POSITIVO

    await reiniciar()

    dut._log.info("PRUEBA 3: Limite X+")

    dut.ui_in.value = 0b00010001

    await esperar(5)

    verificar(0b11000100)

    # PRUEBA 4: LIMITE X NEGATIVO

    await reiniciar()

    dut._log.info("PRUEBA 4: Limite X-")

    dut.ui_in.value = 0b00100001

    await esperar(5)

    verificar(0b11001000)

    # PRUEBA 5: LIMITE Y POSITIVO

    await reiniciar()

    dut._log.info("PRUEBA 5: Limite Y+")

    dut.ui_in.value = 0b01000010

    await esperar(5)

    verificar(0b11010000)

    # PRUEBA 6: LIMITE Y NEGATIVO

    await reiniciar()

    dut._log.info("PRUEBA 6: Limite Y-")

    dut.ui_in.value = 0b10000010

    await esperar(5)

    verificar(0b11100000)

    # PRUEBA 7: LIMITE ACTIVO EN REPOSO

    await reiniciar()

    dut._log.info("PRUEBA 7: Limite en reposo")

    dut.ui_in.value = 0b00010000

    await esperar(5)

    verificar(0b00000000)

    # PRUEBA 8: BLOQUEO MECANICO X

    await reiniciar()

    dut._log.info("PRUEBA 8: Bloqueo X")

    dut.ui_in.value = 0b00000001

    await Timer(
        (TIMEOUT + 10) * PERIODO_NS,
        unit="ns"
    )

    await FallingEdge(dut.clk)

    verificar(0b11000001)

    # PRUEBA 9: BLOQUEO MECANICO Y

    await reiniciar()

    dut._log.info("PRUEBA 9: Bloqueo Y")

    dut.ui_in.value = 0b00001010

    await Timer(
        (TIMEOUT + 10) * PERIODO_NS,
        unit="ns"
    )

    await FallingEdge(dut.clk)

    verificar(0b11000010)

    # PRUEBA 10: MEMORIA DE FALLAS

    dut._log.info("PRUEBA 10: Memoria de fallas")

    dut.ui_in.value = 0b00000000

    await esperar(10)

    verificar(0b11000010)

    # PRUEBA 11: REINICIO FINAL

    await reiniciar()

    dut._log.info("PRUEBA 11: Reinicio")

    verificar(0b00000000)

    # RESULTADO FINAL

    dut._log.info("TODAS LAS PRUEBAS CORRECTAS")
