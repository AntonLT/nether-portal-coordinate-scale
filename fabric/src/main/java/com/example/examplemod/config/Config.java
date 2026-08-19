package com.example.examplemod.config;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonParseException;
import net.fabricmc.loader.api.FabricLoader;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class Config {
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
    private static final Path CONFIG_PATH = FabricLoader.getInstance().getConfigDir().resolve("netherportalcoordinatescale.json");
    private static final double DEFAULT_SCALE = 1.0;
    private static final double MIN_SCALE = 0.01;
    private static final double MAX_SCALE = 64.0;

    public double scale = DEFAULT_SCALE;
    
    private static Config instance;
    
    public static Config getInstance() {
        if (instance == null) {
            load();
        }
        return instance;
    }
    
    private static void load() {
        if (Files.exists(CONFIG_PATH)) {
            try {
                Config loaded = GSON.fromJson(Files.readString(CONFIG_PATH), Config.class);
                instance = loaded == null ? new Config() : loaded;
            } catch (IOException | JsonParseException exception) {
                instance = new Config();
            }
        } else {
            instance = new Config();
            save();
        }
        if (!Double.isFinite(instance.scale) || instance.scale < MIN_SCALE || instance.scale > MAX_SCALE) {
            instance.scale = DEFAULT_SCALE;
        }
    }
    
    private static void save() {
        try {
            Files.createDirectories(CONFIG_PATH.getParent());
            Files.writeString(CONFIG_PATH, GSON.toJson(instance));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
