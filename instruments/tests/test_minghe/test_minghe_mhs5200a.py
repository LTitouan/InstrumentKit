#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module containing tests for the MingHe MHS52000a
"""

# IMPORTS ####################################################################

from __future__ import absolute_import

from nose.tools import raises
import quantities as pq

import instruments as ik
from instruments.tests import expected_protocol, unit_eq


# TESTS ######################################################################


def test_mhs_amplitude():
    with expected_protocol(
        ik.minghe.MHS5200,
        [
            ":r1a",
            ":r2a",
            ":s1a660",
            ":s2a800"
        ],
        [
            ":r1a330",
            ":r2a500",
            "ok",
            "ok"
        ],
        sep="\n"
    ) as mhs:
        assert mhs.channel[0].amplitude == 3.3*pq.V
        assert mhs.channel[1].amplitude == 5.0*pq.V
        mhs.channel[0].amplitude = 6.6*pq.V
        mhs.channel[1].amplitude = 8.0*pq.V


def test_mhs_duty_cycle():
    with expected_protocol(
        ik.minghe.MHS5200,
        [
            ":r1d",
            ":r2d",
            ":s1d6",
            ":s2d8"

        ],
        [
            ":r1d330",
            ":r2d500",
            "ok",
            "ok"
        ],
        sep="\n"
    ) as mhs:
        assert mhs.channel[0].duty_cycle == 330.0*pq.s
        assert mhs.channel[1].duty_cycle == 500.0*pq.s
        mhs.channel[0].duty_cycle = 6*pq.s
        mhs.channel[1].duty_cycle = 8*pq.s


def test_mhs_enable():
    with expected_protocol(
        ik.minghe.MHS5200,
        [
            ":r1b",
            ":r2b",
            ":s1b0",
            ":s2b1"
        ],
        [
            ":r1b1",
            ":r2b0",
            "ok",
            "ok"
        ],
        sep="\n"
    ) as mhs:
        assert mhs.channel[0].enable
        assert not mhs.channel[1].enable
        mhs.channel[0].enable = False
        mhs.channel[1].enable = True


def test_mhs_frequency():
    with expected_protocol(
        ik.minghe.MHS5200,
        [
            ":r1f",
            ":r2f",
            ":s1f6000",
            ":s2f8000"

        ],
        [
            ":r1f33000",
            ":r2f500000",
            "ok",
            "ok"
        ],
        sep="\n"
    ) as mhs:
        assert mhs.channel[0].frequency == 33.0*pq.kHz
        assert mhs.channel[1].frequency == 500.0*pq.kHz
        mhs.channel[0].frequency = 6*pq.kHz
        mhs.channel[1].frequency = 8*pq.kHz


def test_mhs_offset():
    with expected_protocol(
        ik.minghe.MHS5200,
        [
            ":r1o",
            ":r2o",
            ":s1o60",
            ":s2o180"

        ],
        [
            ":r1o120",
            ":r2o0",
            "ok",
            "ok"
        ],
        sep="\n"
    ) as mhs:
        assert mhs.channel[0].offset == 0
        assert mhs.channel[1].offset == -1.2
        mhs.channel[0].offset = -0.6
        mhs.channel[1].offset = 0.6


def test_mhs_phase():
    with expected_protocol(
        ik.minghe.MHS5200,
        [
            ":r1p",
            ":r2p",
            ":s1p60",
            ":s2p180"

        ],
        [
            ":r1p120",
            ":r2p0",
            "ok",
            "ok"
        ],
        sep="\n"
    ) as mhs:
        assert mhs.channel[0].phase == 120
        assert mhs.channel[1].phase == 0
        mhs.channel[0].phase = 60
        mhs.channel[1].phase = 180


def test_mhs_wave_type():
    with expected_protocol(
        ik.minghe.MHS5200,
        [
            ":r1w",
            ":r2w",
            ":s1w2",
            ":s2w3"

        ],
        [
            ":r1w0",
            ":r2w1",
            "ok",
            "ok"
        ],
        sep="\n"
    ) as mhs:
        assert mhs.channel[0].wave_type == mhs.WaveType.sine
        assert mhs.channel[1].wave_type == mhs.WaveType.square
        mhs.channel[0].wave_type = mhs.WaveType.triangular
        mhs.channel[1].wave_type = mhs.WaveType.sawtooth_up


def test_mhs_serial_number():
    with expected_protocol(
        ik.minghe.MHS5200,
        [
            ":r0c"

        ],
        [
            ":r0c5225A1",
        ],
        sep="\n"
    ) as mhs:
        assert mhs.serial_number == "5225A1"