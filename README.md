# Nether Portal Coordinate Scale

A Minecraft mod that automatically scales Nether portal coordinates to match the Overworld, eliminating the need to manually calculate coordinate conversions when traveling between dimensions.

## Features

- **Automatic Coordinate Scaling**: Portals are scaled by 1:8 (or custom ratio) so Nether and Overworld coordinates match
- **Travel Between Dimensions**: No need to calculate coordinate differences when moving between the Nether and Overworld
- **Configurable**: Override the default 1:1 scaling factor in the config file
- **Multi-Loader Support**: Available for both Fabric and NeoForge

## Installation

1. Download the mod JAR for your loader (Fabric or NeoForge)
2. Place it in your `mods` folder
3. Launch Minecraft
4. Configure the scaling factor in `config/netherportalcoordinatescale.json` if needed

## Configuration

Edit `config/netherportalcoordinatescale.json` to adjust the coordinate scaling factor:

```json
{
  "scaling_factor": 1.0
}
```

- `1.0` = 1:1 scaling (coordinates match exactly between dimensions)
- Default uses Minecraft's native 1:8 ratio when not specified

## Links

- [CurseForge](https://www.curseforge.com/minecraft/mods/nether-portal-coordinate-scale)
- [Modrinth](https://modrinth.com/mod/nether-portal-coordinate-scale)

## License

AGPL-3.0 License. See the LICENSE file for details.
