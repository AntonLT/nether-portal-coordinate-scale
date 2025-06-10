package com.example.examplemod.config;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import net.fabricmc.loader.api.FabricLoader;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class Config {
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
    private static final Path CONFIG_PATH = FabricLoader.getInstance().getConfigDir().resolve("netherportalcoordinatescale.json");
    
    public double scale = 1.0; // Default scale value
    
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
                String json = Files.readString(CONFIG_PATH);
                instance = GSON.fromJson(json, Config.class);
            } catch (IOException e) {
                instance = new Config();
            }
        } else {
            instance = new Config();
            save();
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
