// src/main/java/com/alt/netherportalcoordinatescale/config/PortalConfig.java
package com.alt.netherportalcoordinatescale;

import net.minecraftforge.common.ForgeConfigSpec;

public final class PortalConfig {

    /** Forge automatically writes this spec to `<gameDir>/config/one_to_one_portals-common.toml`. */
    public static final ForgeConfigSpec COMMON_SPEC;
    public static final ForgeConfigSpec.DoubleValue NETHER_SCALE;

    static {
        ForgeConfigSpec.Builder b = new ForgeConfigSpec.Builder();

        b.push("coordinate_scale");
        // English comments only – user preference
        NETHER_SCALE = b.comment("""
                Overworld→Nether scale factor.
                1.0 = 1-to-1 (no 8× compression), 0.125 = vanilla.
                Can be hot-reloaded from the config screen or /reload.""")
                .defineInRange("netherScale", 1.0D, 0.01D, 64.0D);
        b.pop();

        COMMON_SPEC = b.build();
    }

    private PortalConfig() {}   // no instantiation
}