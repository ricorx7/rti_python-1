import pytest

from rti_python.Ensemble.Ensemble import Ensemble
from rti_python.Ensemble.Amplitude import Amplitude
from rti_python.Ensemble.Correlation import Correlation
from rti_python.Ensemble.BeamVelocity import BeamVelocity
from rti_python.Ensemble.InstrumentVelocity import InstrumentVelocity
from rti_python.Ensemble.EarthVelocity import EarthVelocity
from rti_python.Ensemble.GoodBeam import GoodBeam
from rti_python.Ensemble.GoodEarth import GoodEarth

def test_generate_header():

    value_type = 10             # Float
    num_elements = 30           # 30 bins
    element_multiplier = 4      # 4 Beams
    imag = 0                    # NOT USED
    name_length = 8             # Length of name
    name = "E000004\0"            # Amp name

    header = Ensemble.generate_header(value_type,
                                      num_elements,
                                      element_multiplier,
                                      imag,
                                      name_length,
                                      name)

    # Value type
    assert 0xA == header[0]
    assert 0x0 == header[1]
    assert 0x0 == header[2]
    assert 0x0 == header[3]

    # Num Elements
    assert 0x1E == header[4]
    assert 0x0 == header[5]
    assert 0x0 == header[6]
    assert 0x0 == header[7]

    # Element Multiplier
    assert 0x4 == header[8]
    assert 0x0 == header[9]
    assert 0x0 == header[10]
    assert 0x0 == header[11]

    # Imag
    assert 0x0 == header[12]
    assert 0x0 == header[13]
    assert 0x0 == header[14]
    assert 0x0 == header[15]

    # Name Length
    assert 0x8 == header[16]
    assert 0x0 == header[17]
    assert 0x0 == header[18]
    assert 0x0 == header[19]

    # Name
    assert ord('E') == header[20]
    assert ord('0') == header[21]
    assert ord('0') == header[22]
    assert ord('0') == header[23]
    assert ord('0') == header[24]
    assert ord('0') == header[25]
    assert ord('4') == header[26]
    assert ord('\0') == header[27]


def test_amplitude():

    amp = Amplitude(30, 4)

    # Populate data
    val = 1.0
    for beam in range(amp.element_multiplier):
        for bin_num in range(amp.num_elements):
            amp.Amplitude[bin_num][beam] = val
            val += 1.1

    result = amp.encode()

    # Value type
    assert 0xA == result[0]
    assert 0x0 == result[1]
    assert 0x0 == result[2]
    assert 0x0 == result[3]

    # Num Elements
    assert 0x1E == result[4]
    assert 0x0 == result[5]
    assert 0x0 == result[6]
    assert 0x0 == result[7]

    # Element Multiplier
    assert 0x4 == result[8]
    assert 0x0 == result[9]
    assert 0x0 == result[10]
    assert 0x0 == result[11]

    # Imag
    assert 0x0 == result[12]
    assert 0x0 == result[13]
    assert 0x0 == result[14]
    assert 0x0 == result[15]

    # Name Length
    assert 0x8 == result[16]
    assert 0x0 == result[17]
    assert 0x0 == result[18]
    assert 0x0 == result[19]

    # Name
    assert ord('E') == result[20]
    assert ord('0') == result[21]
    assert ord('0') == result[22]
    assert ord('0') == result[23]
    assert ord('0') == result[24]
    assert ord('0') == result[25]
    assert ord('4') == result[26]
    assert ord('\0') == result[27]

    # Length
    assert len(result) == 28 + ((amp.element_multiplier * amp.num_elements) * Ensemble.BytesInFloat)

    # Amplitude data
    result_val = 1.0
    index = 28                  # 28 = Header size
    for beam in range(amp.element_multiplier):
        for bin_num in range(amp.num_elements):
            test_val = Ensemble.GetFloat(index, Ensemble().BytesInFloat, bytearray(result))
            assert result_val == pytest.approx(test_val, 0.1)
            result_val += 1.1
            index += Ensemble().BytesInFloat

def test_encode_csv():

    num_bins = 33
    num_beams = 4

    ens = Ensemble()
    amp = Amplitude(num_bins, num_beams)
    corr = Correlation(num_bins, num_beams)
    beam_vel = BeamVelocity(num_bins, num_beams)
    inst_vel = InstrumentVelocity(num_bins, num_beams)
    earth_vel = EarthVelocity(num_bins, num_beams)
    gb = GoodBeam(num_bins, num_beams)
    ge = GoodEarth(num_bins, num_beams)

    ens.AddAmplitude(amp)
    ens.AddCorrelation(corr)
    ens.AddBeamVelocity(beam_vel)
    ens.AddInstrumentVelocity(inst_vel)
    ens.AddEarthVelocity(earth_vel)
    ens.AddGoodBeam(gb)
    ens.AddGoodEarth(ge)

    results = ens.encode_csv()
    total_lines = num_bins * num_beams * 7

    assert len(results) == total_lines
