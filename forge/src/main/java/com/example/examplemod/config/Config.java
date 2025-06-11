// src/main/java/com/example/examplemod/config/ExampleConfig.java
package com.example.examplemod.config;

import net.minecraftforge.common.ForgeConfigSpec;
import net.minecraftforge.fml.config.ModConfig;
import net.minecraftforge.fml.ModLoadingContext;
import org.apache.commons.lang3.tuple.Pair;

/**
 * Holds the Forge config spec and values for the mod.
 */
public final class Config {
    public static final Config INSTANCE;
    public static final ForgeConfigSpec SPEC;

    public final ForgeConfigSpec.DoubleValue SCALE;

    private Config(ForgeConfigSpec.Builder builder) {
        builder.comment("Coordinate scale factor").push("general");
        SCALE = builder.defineInRange("scale", 1.0D, 0.01D, 64.0D);
        builder.pop();
    }

    static {
        Pair<Config, ForgeConfigSpec> pair =
                new ForgeConfigSpec.Builder().configure(Config::new);
        INSTANCE = pair.getLeft();
        SPEC     = pair.getRight();
    }
}