import pyubx2
from pyubx2 import UBXReader

def parse(data: bytes): 
    
    UBXReader.parse(data)
    
    if (sub == 2)
    {
      i = 48;
      eph[sv].iode2 = extract_unsigned(bittbl, i,  8); i +=  8; // Issue of Data (Ephemeris)
      eph[sv].crs   = extract_signed(  bittbl, i, 16); i += 16; // Amplitude of the Sine Harmonic Correction Term to the Orbit Radius
      eph[sv].deln  = extract_signed(  bittbl, i, 16); i += 16;
      eph[sv].m0    = extract_signed(  bittbl, i, 32); i += 32;
      eph[sv].cuc   = extract_signed(  bittbl, i, 16); i += 16; // Amplitude of the Cosine Harmonic Correction Term to the Argument of Latitude
      eph[sv].e     = extract_unsigned(bittbl, i, 32); i += 32;
      eph[sv].cus   = extract_signed(  bittbl, i, 16); i += 16; // Amplitude of the Sine Harmonic Correction Term to the Argument of Latitude
...
      printf("SUB2 %2d %02X\n", sv, eph[sv].iode2);
      _crs  = (double)eph[sv].crs  * (1.0 / 32.0);            // 2^-5
      _deln = (double)eph[sv].deln * (1.0 / 8796093022208.0); // 2^-43
      _m0   = (double)eph[sv].m0   * (1.0 / 2147483648.0);    // 2^-31
      _cuc  = (double)eph[sv].cuc  * (1.0 / 536870912.0);     // 2^-29
      _e    = (double)eph[sv].e    * (1.0 / 8589934592);      // 2^-33
      _cus  = (double)eph[sv].cus  * (1.0 / 536870912.0);     // 2^-29