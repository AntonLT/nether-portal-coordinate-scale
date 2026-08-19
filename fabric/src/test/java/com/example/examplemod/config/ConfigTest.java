package com.example.examplemod.config;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ConfigTest {

    @Test
    void preservesValidScaleValues() {
        assertEquals(0.01, Config.normalizeScale(0.01));
        assertEquals(8.0, Config.normalizeScale(8.0));
        assertEquals(64.0, Config.normalizeScale(64.0));
    }

    @Test
    void defaultsInvalidScaleValues() {
        assertEquals(1.0, Config.normalizeScale(0.009));
        assertEquals(1.0, Config.normalizeScale(64.001));
        assertEquals(1.0, Config.normalizeScale(Double.NaN));
        assertEquals(1.0, Config.normalizeScale(Double.POSITIVE_INFINITY));
    }
}
