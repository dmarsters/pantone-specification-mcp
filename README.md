# Pantone Specification MCP Server

A bridge layer MCP server that translates abstract color concepts from upstream aesthetic domains into production-ready Pantone Graphics (PMS) specifications.

## Role in Lushy Architecture

**Terminal Functor**: This server acts as a terminal object in the Lushy categorical composition system. Multiple upstream domains (heraldic blazonry, cocktail aesthetics, wine tasting, game show aesthetics) functor into Pantone specification, providing reproducible color output for professional production.

```
                    ┌─────────────────┐
                    │   Heraldic      │
                    │   Blazonry      │──────┐
                    └─────────────────┘      │
                                             │
┌─────────────────┐                          ▼
│    Cocktail     │───────────────────► ┌─────────────────┐
│   Aesthetics    │                     │    PANTONE      │
└─────────────────┘                     │  SPECIFICATION  │
                                        │   (Terminal)    │
┌─────────────────┐                     └─────────────────┘
│      Wine       │───────────────────►        │
│    Tasting      │                            │
└─────────────────┘                            ▼
                                        Production-Ready
┌─────────────────┐                     PMS Codes
│   Game Show     │──────┘
│   Aesthetics    │
└─────────────────┘
```

## Features

### Layer 1: Pure Taxonomy (Zero LLM Cost)
- **Colors of the Year (2000-2024)**: Complete Pantone COTY database with era moods, associations, and domain pairings
- **Classic References**: Process colors, metallics, neutrals, heritage colors
- **Era Palettes**: Decade-specific color sets (1950s-2010s) with mood descriptors
- **Domain Mappings**: Pre-defined translations from heraldic, cocktail, and wine vocabularies

### Layer 2: Deterministic Bridge Morphisms (Zero LLM Cost)
- **Heraldic → Pantone**: Tincture to PMS with symbolic preservation (or → 871 C metallic gold)
- **Cocktail → Pantone**: Atmosphere to color temperature with COTY connections
- **Wine → Pantone**: Hue descriptors with age indication preservation
- **Hex → Pantone**: Nearest-neighbor matching with quality metrics
- **Era → Pantone**: Complete temporal palette composition

### Layer 3: Synthesis Support
- Context preparation for Claude creative synthesis
- Intentionality reasoning preservation
- Production warning aggregation

## Installation

```bash
pip install pantone-specification-mcp
```

Or from source:
```bash
git clone https://github.com/lushy/pantone-specification-mcp
cd pantone-specification-mcp
pip install -e .
```

## Usage

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "pantone-specification": {
      "command": "python",
      "args": [
        "/path/to/pantone-specification-mcp/src/pantone_specification_mcp/server.py"
      ]
    }
  }
}
```

### FastMCP Cloud Deployment

Deploy with flattened server structure:
```bash
fastmcp deploy src/pantone_specification_mcp/server.py
```

### Example Tool Calls

**Get Color of the Year:**
```python
get_color_of_the_year(2024)
# Returns: Peach Fuzz (13-1023), era_mood: "gentle_comfort"
```

**Heraldic Bridge:**
```python
specify_pantone_from_heraldic("or", variant="primary", production_context="print_coated")
# Returns: 871 C (Metallic Gold) with production notes about metallic ink
```

**Era Palette:**
```python
compose_era_matched_palette("1970s", include_coty=True)
# Returns: Burnt Orange, Avocado, Harvest Gold, Brown + decade's COTY accents
```

**Universal Bridge:**
```python
bridge_domain_color("wine", "garnet", production_context="print_coated")
# Returns: 188 C (Garnet) with age_indication: "developing"
```

## Data Coverage

| Category | Count | Description |
|----------|-------|-------------|
| Colors of the Year | 25+ | 2000-2024 including dual-color years |
| Classic References | 25+ | Process, metallic, neutral, heritage |
| Era Palettes | 7 | 1950s through 2010s |
| Heraldic Mappings | 9 | All standard tinctures + stains |
| Cocktail Mappings | 7 | Atmosphere types |
| Wine Mappings | 7 | Red and white wine hues |

## Intentionality Principles

### Name Over Number
Pantone names carry cultural weight beyond color values. When selecting between numerically similar options, prefer the one with meaningful name associations.

### Era Authenticity
Historical accuracy requires period-appropriate references. 1970s compositions should use documented 1970s Pantone trend report references.

### Production Honesty
Always acknowledge substrate dependency. Include coated/uncoated distinctions, metallic production requirements, and screen approximation caveats.

### Symbolic Preservation
Source domain symbolism guides selection over ΔE proximity. Heraldic "or" maps to 871 C Metallic Gold (nobility semantic) not 7405 C (closest yellow numerically).

## Production Contexts

- **print_coated** (suffix C): Higher saturation, glossy substrates
- **print_uncoated** (suffix U): Lower saturation, matte substrates, 10-15% saturation loss
- **metallic** (871-877 series): Requires metallic ink or foil stamping, cannot reproduce in CMYK

## Testing

```bash
pytest tests/ -v
```

Test coverage includes:
- Layer 1 taxonomy retrieval
- Layer 2 bridge morphism accuracy
- Intentionality preservation verification
- Production context handling
- Data integrity checks

## API Reference

### Layer 1 Tools
- `list_colors_of_the_year(start_year, end_year)` - COTY database query
- `get_color_of_the_year(year)` - Single COTY lookup
- `list_classic_references(category)` - Classic Pantone catalog
- `get_era_palette(era, include_coty)` - Decade-specific palettes
- `list_heraldic_mappings()` - Tincture translation table
- `list_cocktail_mappings()` - Atmosphere translation table
- `list_wine_mappings()` - Wine hue translation table

### Layer 2 Tools
- `specify_pantone_from_heraldic(tincture, variant, production_context)` - Heraldic bridge
- `specify_pantone_from_cocktail(atmosphere, production_context)` - Cocktail bridge
- `specify_pantone_from_wine(hue, production_context)` - Wine bridge
- `specify_pantone_from_hex(hex_color, production_context, prefer_coty)` - Hex nearest-neighbor
- `match_coty_by_mood(mood, year_range)` - COTY mood search
- `bridge_domain_color(source_domain, color_parameter, production_context, variant)` - Universal router
- `compose_era_matched_palette(era, include_palette, include_coty, production_context)` - Era composition

### Layer 3 Tools
- `prepare_synthesis_context(source_domain, source_parameters, production_context, include_intentionality)` - Claude synthesis prep
- `get_server_info()` - Server metadata

## License

MIT License - see LICENSE file for details.

## Author

Dal Marsters / Lushy Project  
dal@lushy.app

## Related Servers

- [heraldic-blazonry](https://github.com/lushy/heraldic-blazonry) - Heraldic design vocabulary
- [cocktail-aesthetics](https://github.com/lushy/cocktail-aesthetics) - Cocktail atmosphere parameters
- [wine-tasting-mcp](https://github.com/lushy/wine-tasting-mcp) - Wine sensory vocabulary
- [game-show-aesthetics](https://github.com/lushy/game-show-aesthetics) - Era-specific television aesthetics
