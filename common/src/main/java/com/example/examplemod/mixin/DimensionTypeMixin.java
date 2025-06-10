package com.example.examplemod.mixin;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import net.minecraft.world.level.dimension.DimensionType;

@Mixin(DimensionType.class)
public abstract class DimensionTypeMixin {
    @Inject(
            method = "coordinateScale()D",
            at = @At("HEAD"),
            cancellable = true
    )
    private void injectCoordinateScale(CallbackInfoReturnable<Double> cir) {
        if (((DimensionType)(Object)this).toString().toLowerCase().contains("nether")) {
//            double scale = PortalConfig.NETHER_SCALE.get();
            cir.setReturnValue(1.0);
            cir.cancel();
        }
    }
}