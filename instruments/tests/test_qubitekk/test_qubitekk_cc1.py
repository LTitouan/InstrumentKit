#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module containing tests for the Qubitekk CC1
"""

# IMPORTS ####################################################################

from __future__ import absolute_import

from nose.tools import raises
import quantities as pq

import instruments as ik
from instruments.tests import expected_protocol, unit_eq

# TESTS ######################################################################


def test_cc1_count():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "COUN:C1?"
        ],
        [
            "FIRM?",
            "Firmware v2.010",
            "COUN:C1?",
            "20"
        ],
        sep="\n"
    ) as cc:
        assert cc.channel[0].count == 20.0


def test_cc1_window():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "WIND?",
            ":WIND 7"
        ],
        [
            "FIRM?",
            "Firmware v2.010",
            "WIND?",
            "2",
            ":WIND 7"
        ],
        sep="\n"
    ) as cc:
        unit_eq(cc.window, pq.Quantity(2, "ns"))
        cc.window = 7

@raises(ValueError)
def test_cc1_window_error():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            ":WIND 10"
        ],
        [
            "FIRM?",
            "Firmware v2.010",
            ":WIND 10"
        ],
        sep="\n"
    ) as cc:
        cc.window = 10

def test_cc1_delay():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "DELA?",
            ":DELA 2"
        ],
        [
            "FIRM?",
            "Firmware v2.010",
			"DELA?",
            "8",
            ":DELA 2",
            ""
        ],
        sep="\n"
    ) as cc:
        unit_eq(cc.delay, pq.Quantity(8, "ns"))
        cc.delay = 2


@raises(ValueError)
def test_cc1_delay_error1():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            ":DELA -1"
        ],
        [
			"FIRM?",
            "Firmware v2.010",
			":DELA -1"
        ],
        sep="\n"
    ) as cc:
        cc.delay = -1


@raises(ValueError)
def test_cc1_delay_error2():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            ":DELA 1"
        ],
        [
			"FIRM?",
            "Firmware v2.010",
			":DELA 1"
        ],
        sep="\n"
    ) as cc:
        cc.delay = 1


def test_cc1_dwell_old_firmware():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "DWEL?",
            ":DWEL 2"
        ],
        [
            "Firmware v2.001",
            "8000",
			""
        ],
        sep="\n"
    ) as cc:
        unit_eq(cc.dwell_time, pq.Quantity(8, "s"))
        cc.dwell_time = 2


def test_cc1_dwell_new_firmware():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "DWEL?",
            ":DWEL 2"
        ],
        [
            "FIRM?",
            "Firmware v2.010",
            "DWEL?",
            "8",
            ":DWEL 2"
        ],
        sep="\n"
    ) as cc:
        unit_eq(cc.dwell_time, pq.Quantity(8, "s"))
        cc.dwell_time = 2


@raises(ValueError)
def test_cc1_dwell_time_error():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            ":DWEL -1"
        ],
        [
			"FIRM?",
            "Firmware v2.010",
            ":DWEL -1"
        ],
        sep="\n"
    ) as cc:
        cc.dwell_time = -1


def test_cc1_firmware():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?"
        ],
        [
			"FIRM?",
            "Firmware v2.010"
        ],
        sep="\n"
    ) as cc:
        assert cc.firmware == (2, 10, 0)


def test_cc1_firmware_2():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?"
        ],
        [
            "Firmware v2"
        ],
        sep="\n"
    ) as cc:
        assert cc.firmware == (2, 0, 0)


def test_cc1_firmware_3():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?"
        ],
        [
			"FIRM?",
            "Firmware v2.010.1"
        ],
        sep="\n"
    ) as cc:
        assert cc.firmware == (2, 10, 1)


def test_cc1_firmware_repeat_query():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "FIRM?"
        ],
        [
			"FIRM?",
            "Unknown",
			"FIRM?",
            "Firmware v2.010"
        ],
        sep="\n"
    ) as cc:
        assert cc.firmware == (2, 10, 0)


def test_cc1_gate_new_firmware():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "GATE?",
            ":GATE:ON",
            ":GATE:OFF"

        ],
        [
			"FIRM?",
            "Firmware v2.010",
            "GATE?",
            "ON",
            ":GATE:ON",
            ":GATE:OFF"
        ],
    ) as cc:
        assert cc.gate is True
        cc.gate = True
        cc.gate = False

def test_cc1_gate_old_firmware():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "GATE?",
            ":GATE 1",
            ":GATE 0"

        ],
        [
            "Firmware v2.001",
            "1",
            "",
            ""
        ],
        sep="\n"
    ) as cc:
        assert cc.gate is True
        cc.gate = True
        cc.gate = False


@raises(TypeError)
def test_cc1_gate_error():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            ":GATE blo"
        ],
        [
            "FIRM?",
            "Firmware v2.010",
			":GATE blo"
        ],
        sep="\n"
    ) as cc:
        cc.gate = "blo"


def test_cc1_subtract_new_firmware():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "SUBT?",
            ":SUBT:ON",
            ":SUBT:OFF"

        ],
        [
            "FIRM?",
            "Firmware v2.010",
            "SUBT?",
            "ON",
			":SUBT:ON",
            ":SUBT:OFF"
        ],
        sep="\n"
    ) as cc:
        assert cc.subtract is True
        cc.subtract = True
        cc.subtract = False


@raises(TypeError)
def test_cc1_subtract_error():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            ":SUBT blo"

        ],
        [
            "FIRM?",
            "Firmware v2.010",
            ":SUBT blo"
        ],
        sep="\n"
    ) as cc:
        cc.subtract = "blo"


def test_cc1_trigger_mode():  # pylint: disable=redefined-variable-type
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "TRIG?",
            ":TRIG:MODE CONT",
            ":TRIG:MODE STOP"
        ],
        [
            "FIRM?",
            "Firmware v2.010",
            "TRIG?",
            "MODE STOP",
            ":TRIG:MODE CONT",
            ":TRIG:MODE STOP"
        ],
        sep="\n"
    ) as cc:
        assert cc.trigger_mode is cc.TriggerMode.start_stop
        cc.trigger_mode = cc.TriggerMode.continuous
        cc.trigger_mode = cc.TriggerMode.start_stop


def test_cc1_trigger_mode_old_firmware():  # pylint: disable=redefined-variable-type
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "TRIG?",
            ":TRIG 0",
            ":TRIG 1"
        ],
        [
            "Firmware v2.001",
            "1",
            "",
            ""
        ],
        sep="\n"
    ) as cc:
        assert cc.trigger_mode == cc.TriggerMode.start_stop
        cc.trigger_mode = cc.TriggerMode.continuous
        cc.trigger_mode = cc.TriggerMode.start_stop


@raises(ValueError)
def test_cc1_trigger_mode_error():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?"
        ],
        [
            "FIRM?",
			"Firmware v2.010"
        ],
        sep="\n"
    ) as cc:
        cc.trigger_mode = "blo"


def test_cc1_clear():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "CLEA"
        ],
        [
            "FIRM?",
            "Firmware v2.010",
			"CLEA"
        ],
        sep="\n"
    ) as cc:
        cc.clear_counts()