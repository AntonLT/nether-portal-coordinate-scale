// src/main/java/com/example/examplemod/config/ExampleConfig.java
package com.example.examplemod.config;

import net.neoforged.neoforge.common.ModConfigSpec;
import org.apache.commons.lang3.tuple.Pair;

public final class Config {
    // The object holding your config values
    public static final Config INSTANCE;
    // The TOML spec that NeoForge will read/write
    public static final ModConfigSpec SPEC;

    // Your actual config entry
    public final ModConfigSpec.DoubleValue SCALE;

    private Config(ModConfigSpec.Builder builder) {
        // optional: push/pop sections if you want subsections
        builder.comment("Coordinate scale factor for nether portal teleportation");
        SCALE = builder.defineInRange("scale", 1.0, 0.01, 64.0);
    }

    static {
        // Builds both the ExampleConfig instance and the ModConfigSpec in one go  [oai_citation:0‡docs.neoforged.net](https://docs.neoforged.net/docs/misc/config/)
        Pair<Config, ModConfigSpec> pair =
                new ModConfigSpec.Builder().configure(Config::new);
        INSTANCE = pair.getLeft();
        SPEC     = pair.getRight();
    }
}