package com.example.examplemod.config;

import com.example.examplemod.Constants;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonParseException;
import net.fabricmc.loader.api.FabricLoader;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class Config {
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
    
    public double scale = 1.0; // Default scale value
    
    private static Config instance;
    
    public static Config getInstance() {
        if (instance == null) {
            load();
        }
        return instance;
    }
    
    private static void load() {
        Path configPath = configPath();
        if (Files.exists(configPath)) {
            try {
                Config loaded = GSON.fromJson(Files.readString(configPath), Config.class);
                if (loaded == null) {
                    throw new JsonParseException("Config is empty");
                }
                double normalized = normalizeScale(loaded.scale);
                if (normalized != loaded.scale) {
                    Constants.LOG.warn("Invalid portal coordinate scale {}; using 1.0", loaded.scale);
                    loaded.scale = normalized;
                }
                instance = loaded;
            } catch (IOException | JsonParseException e) {
                Constants.LOG.warn("Could not load {}; using defaults", configPath, e);
                instance = new Config();
            }
        } else {
            instance = new Config();
            save();
        }
    }
    
    private static void save() {
        Path configPath = configPath();
        try {
            Files.createDirectories(configPath.getParent());
            Files.writeString(configPath, GSON.toJson(instance));
        } catch (IOException e) {
            Constants.LOG.warn("Could not save {}", configPath, e);
        }
    }

    private static Path configPath() {
        return FabricLoader.getInstance().getConfigDir().resolve("netherportalcoordinatescale.json");
    }

    static double normalizeScale(double scale) {
        return Double.isFinite(scale) && scale >= 0.01 && scale <= 64.0 ? scale : 1.0;
    }
}
