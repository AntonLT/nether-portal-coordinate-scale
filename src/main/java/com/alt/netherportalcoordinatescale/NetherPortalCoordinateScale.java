package com.alt.netherportalcoordinatescale;

import com.mojang.logging.LogUtils;
import net.minecraftforge.fml.ModLoadingContext;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.config.ModConfig;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import org.slf4j.Logger;

@Mod(NetherPortalCoordinateScale.MODID)
public class NetherPortalCoordinateScale
{
    public static final String MODID = "netherportalcoordinatescale";
    private static final Logger LOGGER = LogUtils.getLogger();
    public NetherPortalCoordinateScale() {
        ModLoadingContext.get().registerConfig(
                ModConfig.Type.COMMON, PortalConfig.COMMON_SPEC, MODID + ".toml");

    }
}
