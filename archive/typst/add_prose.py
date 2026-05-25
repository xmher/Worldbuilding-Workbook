#!/usr/bin/env python3
"""Add missing prose content from the markdown source to 01_geography.json.

This script inserts all the prose paragraphs, Common Mistakes, Common Geographic
Patterns tables, Naming Places intro, "How to write it" guidance, and the
Pressure Cooker detail content that exist in the markdown but are missing from
the JSON data file.
"""

import json
from pathlib import Path

DATA = Path(__file__).parent / "data" / "01_geography.json"

with open(DATA) as f:
    data = json.load(f)

content = data["content"]


def find_index(type_val, text_substring=None, start=0):
    """Find index of a content item by type and optional text substring."""
    for i in range(start, len(content)):
        if content[i].get("type") == type_val:
            if text_substring is None:
                return i
            if text_substring in content[i].get("text", ""):
                return i
    raise ValueError(f"Could not find {type_val} with '{text_substring}' from index {start}")


def insert_after(idx, items):
    """Insert items after the given index. Returns new index after inserted items."""
    for i, item in enumerate(items):
        content.insert(idx + 1 + i, item)
    return idx + len(items)


# ============================================================
# 1. After the anchor_card (Pressure Cooker), add the detail content
# ============================================================
idx = find_index("anchor_card")
insert_after(idx, [
    {"type": "prose", "text": "The key is that *leaving must be impossible, dangerous, or carry unacceptable consequences*. When characters can't escape each other, they're forced to confront conflict instead of avoiding it, rely on each other despite distrust, and share space long enough for attraction to build beneath their defenses."},
    {"type": "prose", "text": "Think about what makes the container seal tight:"},
    {"type": "bullet_list", "items": [
        "**Physical trapping:** Islands, academies, sieges, ships, remote estates — locations with literal boundaries characters cannot cross",
        "**Circumstantial trapping:** Dangerous wilderness requiring partnership, diplomatic missions, shared exile — situations where separating means failure or death",
        "**Environmental trapping:** Storms, seasons, magical barriers that prevent departure — external forces that make leaving impossible regardless of desire",
        "**Social/political trapping:** Arranged marriages, hostage situations, court obligations — circumstances where leaving would destroy reputation, alliance, or lives",
    ]},
    {"type": "prose", "text": "The pressure cooker works because proximity breeds intimacy. Characters see each other at their worst. They can't maintain facades. Small moments accumulate — shared meals, overheard conversations, accidental touches in tight quarters. The setting does half the work of bringing them together."},
    {"type": "hint", "text": "**The Key Question:** If your characters could simply walk away from each other, would they? If yes, your geography might need to make walking away impossible, dangerous, or costly."},
])

# ============================================================
# 2. Add "Common Geographic Patterns in Romantasy" section
# ============================================================
# Insert before the divider that precedes "Reference: Place Name Patterns"
idx = find_index("heading2", "Reference: Place Name Patterns")
# Go back to find the divider before it
div_idx = idx - 1
while div_idx >= 0 and content[div_idx].get("type") != "divider":
    div_idx -= 1

insert_after(div_idx, [
    {"type": "divider"},
    {"type": "heading2", "text": "Common Geographic Patterns in Romantasy"},
    {"type": "heading3", "text": "Settings That Force Proximity"},
    {
        "type": "data_table",
        "headers": ["Setting Type", "Why It Works", "Examples"],
        "rows": [
            ["**The Academy/Training Ground**", "Characters live, train, and compete in close quarters with no escape", "*Fourth Wing*, *Zodiac Academy*"],
            ["**The Isolated Estate**", "Limited cast, limited space, limited options for avoidance", "Gothic romances, *Pride and Prejudice* variations"],
            ["**The Ship/Caravan**", "Moving container with enforced proximity and shared danger", "Pirate romance, trade caravan stories"],
            ["**The Siege/War Camp**", "External threat forces cooperation; death is the alternative", "Military romantasy"],
            ["**The Prison/Captivity**", "Hostage and captor, shared cell, or trapped in enemy territory together", "Captive romance, enemies-to-lovers"],
            ["**The Dangerous Quest**", "Mission requires partnership; separating means failure or death", "Quest narratives, escort missions"],
            ["**The Snowed-In/Stranded**", "Weather or disaster traps characters until conditions change", "Cabin romance, \"only one bed\""],
            ["**The Royal Court**", "Political obligations, arranged proximity, can't leave without scandal", "Court intrigue, political marriage"],
        ],
    },
    {"type": "heading3", "text": "Geographic Barriers That Create Stakes"},
    {
        "type": "data_table",
        "headers": ["Barrier Type", "Romantic Function", "Story Possibilities"],
        "rows": [
            ["**Mountain ranges**", "Separate nations/cultures; make travel seasonal", "Characters from opposite sides; winter trapping"],
            ["**Oceans**", "Create complete separation; make departure permanent", "Letters across distance; the weight of leaving"],
            ["**Deserts**", "Isolate cultures; make resources precious", "Oasis politics; survival journeys"],
            ["**Magical borders**", "Can be crossed only by certain people or under certain conditions", "One character can cross, one cannot"],
            ["**War zones**", "Make travel deadly; create no-man's-land between peoples", "Enemies from opposing sides"],
            ["**Political borders**", "Crossing means treason or exile", "Forbidden love across enemy lines"],
            ["**Cursed/Blighted lands**", "Regions too dangerous to cross; require special protection", "Must find another way; one character immune, one isn't"],
            ["**Class geography**", "Slums vs. palace district; social ruin to cross", "Wrong-side-of-tracks romance; secret meetings in between spaces"],
        ],
    },
    {"type": "heading3", "text": "Environmental Conditions That Affect Romance"},
    {
        "type": "data_table",
        "headers": ["Condition", "How It Creates Pressure", "Romantic Beats It Enables"],
        "rows": [
            ["**Harsh winters**", "Traps characters indoors; requires shared warmth", "Forced proximity; \"snowed in\" scenarios"],
            ["**Dangerous nights**", "Characters must shelter together after dark", "Shared watch; protective sleeping arrangements"],
            ["**Seasonal access**", "Passes close, ships can't sail, travel becomes impossible", "Racing against time; trapped until spring"],
            ["**Resource scarcity**", "Sharing becomes necessary; generosity becomes meaningful", "Sharing food/water; sacrifice for the other"],
            ["**Extreme heat**", "Travel only possible at night; requires shade-sharing, water rationing", "Night travel intimacy; sharing precious water; heat exhaustion care"],
            ["**Hostile territory after dark**", "Monsters or predators hunt at night; must camp together for safety", "One bed/bedroll situations; taking turns on watch; protective instincts"],
            ["**Corrupted/poisoned land**", "Regions that drain magic or health; must move quickly or rely on healer", "Dependency on one character's abilities; racing against deterioration"],
        ],
    },
])

# ============================================================
# 3. Add "Common Mistakes with Geographic Worldbuilding" section
# ============================================================
# Find the newly inserted "Common Geographic Patterns" and the patterns tables
# Insert after the last data_table of Common Geographic Patterns
idx = find_index("heading2", "Common Geographic Patterns")
# Find the next divider or heading2 after it
j = idx + 1
while j < len(content) and content[j].get("type") not in ("divider", "heading2") or (content[j].get("type") == "heading3"):
    j += 1

insert_after(j - 1, [
    {"type": "divider"},
    {"type": "heading2", "text": "Common Mistakes with Geographic Worldbuilding"},
    {
        "type": "mistake_box",
        "title": "Mistake #1: The Teleporting World",
        "body": "Characters travel vast distances with no sense of time passing. A journey that should take weeks happens between chapters with no mention of how they traveled or what dangers they faced. Distance has no weight. Separation has no stakes. Reunion carries no emotional punch.",
        "fix": "Establish travel times and stick to them. The journey itself can be where the romance happens.",
    },
    {
        "type": "mistake_box",
        "title": "Mistake #2: The Convenient Geography",
        "body": "Geographic features appear or disappear based on plot needs. A mountain range exists when you need to separate characters but vanishes when they need to reunite. Readers notice. Stakes that feel fake are stakes that don't matter.",
        "fix": "Establish your geography early and let it constrain you. Let the physical world create problems you didn't plan for — those problems often generate the best scenes.",
    },
    {
        "type": "mistake_box",
        "title": "Mistake #3: The Empty Map",
        "body": "You have a map with named places, but none feel lived-in. The geography exists but doesn't affect anything. Geography should create culture, which creates characters, which creates conflict. If your geography doesn't explain why people are the way they are, your world is just a painted backdrop.",
        "fix": "For every major geographic feature, ask: *How does this shape the people who live here?* Let geography explain cultural difference.",
    },
    {
        "type": "mistake_box",
        "title": "Mistake #4: The Consequence-Free Environment",
        "body": "Your world has dangerous regions and deadly terrain — but no one suffers consequences from them. Characters trek through the Deadly Wastes and emerge fine. If danger is all threat and no delivery, readers stop believing in it. And if readers don't believe the world is dangerous, they don't believe your characters need each other to survive it.",
        "fix": "Let the environment actually hurt people. Show consequences — exhaustion, injury, loss. Make survival meaningful.",
    },
    {
        "type": "mistake_box",
        "title": "Mistake #5: Geography Without Emotional Resonance",
        "body": "You describe the setting in detail, but it's all physical — mountains are tall, forests are dense, cities are crowded. None of it connects to how your characters feel. Setting should be emotional landscape. The place where they first met should feel different than other places. The character's homeland should feel like *home*.",
        "fix": "Give each major location an emotional quality, and let characters experience it differently. The same castle might feel like prison to one character and sanctuary to another.",
    },
])

# ============================================================
# 4. Add "Reference: Travel Times" table in concepts section
# ============================================================
# Insert before the Common Geographic Patterns section (after Common Mistakes)
idx = find_index("heading2", "Common Mistakes")
# Find end of mistakes section
j = idx + 1
while j < len(content) and content[j].get("type") != "divider":
    j += 1

insert_after(j - 1, [
    {"type": "divider"},
    {"type": "heading2", "text": "Reference: Travel Times (Fantasy Approximations)"},
    {
        "type": "data_table",
        "headers": ["Mode of Travel", "Distance per Day", "Notes"],
        "rows": [
            ["Walking (easy terrain)", "15-20 miles", "Healthy adult, good weather"],
            ["Walking (difficult terrain)", "8-12 miles", "Mountains, forest, desert"],
            ["Horseback (sustainable)", "25-35 miles", "Without exhausting the horse"],
            ["Horseback (hard riding)", "50-60 miles", "Cannot maintain long-term"],
            ["Ship (sailing)", "100-150 miles", "Dependent on wind and current"],
            ["Carriage/wagon", "20-30 miles", "Roads required; slower on rough terrain"],
        ],
    },
])

# ============================================================
# 5. Add Naming Places intro prose
# ============================================================
idx = find_index("heading2", "Reference: Place Name Patterns")
insert_after(idx, [
    {"type": "prose", "text": "Good place names make your world feel real. You don't need to invent a whole language — just notice how real places get their names."},
    {"type": "prose", "text": "Most names come from geography (Blackwood, Riverside), historical figures (Washington), or descriptions in old languages (Oxford means \"ford where oxen cross\"). Borrow the patterns, not the exact words."},
    {"type": "heading3", "text": "How to Research Naming Conventions"},
    {"type": "prose", "text": "Want to create place names that evoke a particular culture or aesthetic? Here's how to find patterns yourself:"},
    {"type": "prose", "text": "**Quick Research Methods**"},
    {"type": "bullet_list", "items": [
        "**Search \"[language] place name meanings\"** — e.g., \"Old Norse place name meanings\" or \"Welsh place name elements\"",
        "**Search \"[language] words for [terrain]\"** — e.g., \"Japanese words for mountain\" or \"Gaelic words for river\"",
        "**Look up real places** — Search \"etymology of [real place name]\" to see how actual names were constructed",
        "**Wikipedia's toponymy pages** — Search \"[language] toponymy\" for organized lists of place name elements",
        "**Behind the Name** — The website behindthename.com has a place names section with etymologies",
    ]},
    {"type": "prose", "text": "For deeper language work, see *Section 11: Language & Communication*."},
])

# ============================================================
# 6. Add prose intros for Kingdoms & Nations
# ============================================================
idx = find_index("heading2", "Kingdoms & Nations")
insert_after(idx, [
    {"type": "prose", "text": "Got multiple kingdoms or nations in your world? This table helps you keep track of them."},
    {"type": "prose", "text": "You don't need to fill in every field. Just jot down what you know right now. Perhaps you only know the name and climate — that's fine. You can always come back later as your story takes shape."},
])

# ============================================================
# 7. Add prose intro for Terrain Types
# ============================================================
idx = find_index("heading2", "Terrain Types")
insert_after(idx, [
    {"type": "prose", "text": "Not every terrain needs equal development. Consider what exists in your world — *mountains, forests, deserts, plains, wetlands, coastlines, islands, rivers, tundra, magical or unusual terrain* — then focus on the 2-3 that actually matter for your story: the ones your characters traverse, fight over, or call home."},
])

# ============================================================
# 8. Add prose intro for Resources & Territorial Control
# ============================================================
idx = find_index("heading2", "Resources & Territorial Control")
insert_after(idx, [
    {"type": "prose", "text": "Geography determines who has what — and therefore, who has power. Fertile land, fresh water, mineral deposits, trade routes: these are worth fighting over, worth marrying for, worth dying for."},
    {"type": "prose", "text": "In romantasy, resource control can create power imbalances that drive conflict between our two (or more) love interests. Resource control is a believable tactic to explain arranged marriages, political alliances, or economic pressures that force characters to make impossible choices."},
    {"type": "hint", "text": "**How to write it:** Don't explain resource conflict through exposition — show it through what characters can and can't do. A character from a water-scarce region might flinch at seeing someone leave a bath running. Someone from contested territory notices strategic value in landscape others see as beautiful. Let resource awareness emerge through small reactions, casual comments about price or scarcity, and the background hum of what everyone in this world worries about. When two characters come from opposite sides of a resource conflict, show the tension through what they assume about each other, what they're careful not to say, and the moments when privilege becomes visible."},
])

# ============================================================
# 9. Add prose intro for The Sensory World
# ============================================================
idx = find_index("heading2", "The Sensory World")
insert_after(idx, [
    {"type": "prose", "text": "Geography isn't just about what's there — it's about what it feels like to be there. The sensory details of your setting create the emotional texture of scenes. A first kiss hits differently in a garden heavy with night-blooming jasmine than in a stone corridor that smells of torch smoke."},
    {"type": "hint", "text": "**How to write it:** Filter sensory details through your POV character's emotional state. A character falling in love notices the warmth of sunlight, the sweet smell of blossoms, the softness of grass. The same garden, to a grieving character, might feel too bright, the flowers cloying, the birdsong intrusive. You don't need to describe everything — pick 2-3 sensory details per scene that reinforce the mood you're creating."},
    {"type": "prose", "text": "Avoid the \"weather report\" opening (starting scenes with neutral descriptions of setting). Instead, integrate sensory details into action and emotion: not \"The room was cold\" but \"She pulled her cloak tighter, breath misting in the unheated chamber.\" The character's interaction with the environment reveals both setting and feeling simultaneously."},
])

# ============================================================
# 10. Add prose intro for Climate, Weather & Seasons
# ============================================================
idx = find_index("heading2", "Climate, Weather & Seasons")
insert_after(idx, [
    {"type": "prose", "text": "Weather creates immediate physical conditions that affect what's possible — travel, agriculture, warfare, daily life. Seasons can function as deadlines (they must marry before winter closes the pass), as waiting periods (trapped together until spring thaw), or as markers of time passing in a slow-burn romance."},
    {"type": "hint", "text": "**How to write it:** Use seasonal markers to show time passing without stating it directly — the first frost, the smell of rain after months of drought, the angle of afternoon light. Weather works best when it creates immediate physical problems: wet clothing that must be removed, cold that requires shared warmth, heat that makes tempers short. Don't just describe weather — show characters adapting to it, complaining about it, making decisions around it. A change in season can mirror emotional shifts: a relationship that thaws as winter ends, tension that builds with summer heat, a reckoning that arrives with autumn."},
])

# ============================================================
# 11. Add prose intro for Dangerous Regions
# ============================================================
idx = find_index("heading2", "Dangerous Regions")
insert_after(idx, [
    {"type": "prose", "text": "Every world has places that are deadly — and therefore avoided, or crossed only with preparation and company. Dangerous regions serve romance by raising stakes and forcing partnership."},
])

# ============================================================
# 12. Add prose intro for Home & Belonging
# ============================================================
idx = find_index("heading2", "Home & Belonging")
insert_after(idx, [
    {"type": "prose", "text": "Geography isn't just physical — it's emotional. Home is one of the most emotionally charged concepts in romance. Characters may leave home to find love, may be torn between love and home, may find that home becomes wherever the other person is — or may discover that choosing this person means exile from everything familiar."},
    {"type": "hint", "text": "**How to write it:** Show home through specific, sensory details rather than telling readers a place matters. What does your character reach for when they're homesick? What smell instantly transports them back? When writing scenes set in a character's home territory, let them move through space with ease and familiarity — they know which floorboard creaks, which window sticks. Contrast this with how they move through unfamiliar spaces: hesitant, observant, slightly off-balance. The tension between \"where I belong\" and \"where love is taking me\" creates some of romance's most powerful emotional beats."},
])

# ============================================================
# 13. Add prose intro for Entering Each Other's Worlds
# ============================================================
idx = find_index("heading2", "Entering Each Other's Worlds")
insert_after(idx, [
    {"type": "prose", "text": "If your characters come from different places, visiting each other's territory is significant. There's a particular vulnerability in bringing someone into your home territory. You see your world through their eyes, noticing things you'd stopped seeing — both the beauty and the flaws."},
    {"type": "hint", "text": "**How to write it:** When a character enters their love interest's world, filter every observation through their outsider perspective. What confuses them? What impresses them? What makes them uncomfortable? Use their reactions to reveal both the world and the character. The \"native\" character, meanwhile, experiences a different kind of vulnerability — suddenly aware of poverty they'd normalized, privilege they'd taken for granted, or customs that seem strange when explained aloud. Write the small moments: the love interest automatically reaching to help with something the visitor doesn't know how to do, the visitor mispronouncing a word everyone here knows, the native defending their home against a criticism they privately agree with. These fish-out-of-water scenes build intimacy because they require explanation, patience, and the trust to look foolish in front of someone."},
])

# ============================================================
# 14. Add prose intro for Travel & Distance
# ============================================================
idx = find_index("heading2", "Travel & Distance")
insert_after(idx, [
    {"type": "prose", "text": "Distance creates stakes. If characters can teleport anywhere, separation has no weight. If journeys take weeks, every departure matters."},
    {"type": "hint", "text": "**How to write it:** The journey is not filler between plot points — it's where relationships transform. Travel strips away social roles and forces characters into shared vulnerability: sleeping near each other, seeing each other tired and irritable, depending on each other for survival or navigation. Use the physical demands of travel to create intimacy: one character tending another's blisters, sharing body heat in cold camps, the enforced proximity of a small boat or narrow trail. Write the rhythm of travel — the silence that becomes comfortable, the conversations that only happen when there's nothing else to do, the way danger bonds people faster than safety ever could. When writing separation across distance, make the weight felt through what characters can't do: letters that arrive too late, news that travels slowly, the agony of not knowing. A reunion after real distance hits harder than one after a brief absence."},
])

# ============================================================
# 15. Add prose intro for Isolated Locations
# ============================================================
idx = find_index("heading2", "Isolated Locations")
insert_after(idx, [
    {"type": "prose", "text": "Isolation is romance's secret weapon. When characters cannot leave, they cannot avoid each other — and avoidance is the enemy of romantic development. Isolated settings force confrontation, require cooperation, and create the pressure that transforms reluctant attraction into something undeniable."},
    {"type": "hint", "text": "**How to write it:** Establish early why leaving isn't an option, and make that reason feel real and insurmountable. Then use the confined space intentionally: the only warm room where everyone gathers, the narrow hallways where characters keep brushing past each other, the shared resources that require negotiation. Write the claustrophobia alongside the intimacy — isolation can feel oppressive, and characters might resent their forced proximity even as attraction builds. The best isolated-setting romances use the location's specific constraints: a ship means someone must keep watch, an academy means competitive dynamics, a snowed-in estate means dwindling supplies. Let the setting generate plot. And remember: when characters finally could leave but choose to stay, that choice becomes a declaration."},
])

# ============================================================
# 16. Add prose intro for Geography as Emotional Landscape
# ============================================================
idx = find_index("heading2", "Geography as Emotional Landscape")
insert_after(idx, [
    {"type": "prose", "text": "The physical world can resonate with or contrast against the emotional journey. A love scene in a sunlit meadow feels different than one in a crumbling tower. A confession during a storm carries different weight than one in stillness."},
    {"type": "hint", "text": "**How to write it:** Match or intentionally contrast your setting with emotional beats. A first kiss in a dangerous place carries urgency; the same kiss in a peaceful garden suggests safety and choice. Use pathetic fallacy sparingly but effectively — a storm during a confrontation, sunlight breaking through as characters reconcile. More subtly, let characters notice their environment differently based on emotional state: a character in love sees beauty everywhere; a heartbroken character finds the same landscape bleak. Create \"their place\" — a location that becomes sacred to the relationship, whether it's where they first met, first kissed, or survived something together. When characters return to meaningful locations, the resonance should be felt without being over-explained. A single line — \"She hadn't been back to the bridge since that night\" — can carry enormous weight if you've built the association."},
])

# ============================================================
# 17. Add Map Making intro prose + tools
# ============================================================
# Map Making is inside a group at the end. We need to expand it.
# Find the group that contains "Map Making"
map_group_idx = None
for i, c in enumerate(content):
    if c.get("type") == "group":
        for ch in c.get("content", []):
            if "Map Making" in ch.get("text", ""):
                map_group_idx = i
                break
    if map_group_idx is not None:
        break

if map_group_idx is not None:
    # Extract the group's content
    old_group = content[map_group_idx]
    old_children = old_group.get("content", [])
    # Replace with expanded content: intro prose, tools, then original table content
    new_items = [
        {"type": "heading2", "text": "Map Making (Optional)"},
        {"type": "prose", "text": "You don't need a map. Plenty of great fantasy stories were written without one."},
        {"type": "prose", "text": "That said, maps can help you keep travel times consistent and visualize where things are in relation to each other. If you decide to make one, let your story's needs guide you."},
        {"type": "prose", "text": "For example: How far is the border your characters are fleeing toward? Is the palace defensible? Where might lovers meet in secret? Build your geography around the situations your plot requires."},
        {"type": "heading4", "text": "Map-Making Tools"},
        {"type": "hint", "text": "Free options unless noted. Search these names online for current links."},
        {"type": "bullet_list", "items": [
            "**Inkarnate** — Popular fantasy map maker (free tier available)",
            "**Azgaar's Fantasy Map Generator** — Procedural generation with editing",
            "**Wonderdraft** — One-time purchase, professional quality",
            "**Donjon** — Random generators for maps and dungeons",
            "**World Anvil** — Worldbuilding wiki with map tools (subscription)",
        ]},
    ]
    # Re-wrap old table content into a group (heading4 "What to Include" + hint + table)
    new_items.append({
        "type": "group",
        "content": [
            {"type": "heading4", "text": "What to Include on Your Map"},
            old_children[1],  # hint
            old_children[2],  # data_table
        ],
    })
    # Replace the old group with all new items
    content[map_group_idx:map_group_idx+1] = new_items

    # Add final thought at the end
    content.append({"type": "hint", "text": "**Final Thought:** Your map isn't just where things are — it's why characters must make the choices they make. The mountain range is why two nations distrust each other. The desert is why whoever controls the oasis controls the trade route. Build geography that explains your world and creates the situations your story needs."})

# ============================================================
# 19. Add Part One / Part Two divider headings
# ============================================================
# Find "The Big Picture" and insert Part One heading before it
idx = find_index("heading2", "The Big Picture")
# Go back to find the divider before it
div_idx = idx - 1
while div_idx >= 0 and content[div_idx].get("type") != "divider":
    div_idx -= 1
if div_idx >= 0:
    insert_after(div_idx, [
        {"type": "heading2", "text": "Part One — The Foundation"},
    ])

# Find "Home & Belonging" and insert Part Two heading before it
idx = find_index("heading2", "Home & Belonging")
# Go back to find the divider before it
div_idx = idx - 1
while div_idx >= 0 and content[div_idx].get("type") != "divider":
    div_idx -= 1
if div_idx >= 0:
    insert_after(div_idx, [
        {"type": "heading2", "text": "Part Two — Geography & Romance"},
    ])

# Write the updated JSON
with open(DATA, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Done. Content items: {len(content)}")
