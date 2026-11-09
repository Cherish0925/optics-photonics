# pic

Separate geometric layout, electromagnetic component response and circuit network calculation. gdsfactory, KLayout, Nazca, SiEPIC and IPKISS describe layout and PDK conventions; Meep/Lumerical/JCMsuite/Tidy3D provide component modes and scattering; SAX, INTERCONNECT, VPI and related tools compose networks.

Preserve layer/datatype, database unit, port position/orientation, mode order, polarization, reference planes and S-parameter frequency grid. A GDS file does not identify a manufacturable process without a PDK and layer stack. Record the PDK release and run its own design-rule checks. Compare passivity and reciprocity only where the physical device warrants them. Keep amplitude and power normalization distinct. A circuit model should carry its fit range, temperature and geometry parameters; do not extrapolate resonant behavior silently.

Use software_details for the selected tool’s primary documentation and implementation links.
