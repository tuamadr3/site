import re

original_index_html_style_content = """
/* ... (html, body, .snap-container, .snap-container section styles) ... */
/* General snap-container section style that might be relevant */
.snap-container section {
    height: 100vh; /* Each section is full viewport height */
    width: 100%;   /* Each section is full viewport width */
    scroll-snap-align: start; /* Snap to the start of each section */
    display: flex;
    align-items: center;
}

#section2 {
    background-color: #FFFFFF; /* White */
    color: #333333;           /* Dark grey text */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 40px 5%;
    box-sizing: border-box;
}
.slide-content-container { /* General container for slide content if needed for structure */
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.pimpa-story h2 {
    font-size: 2.2em;
    font-weight: bold;
    color: #337ab7;
    margin-bottom: 30px;
    text-align: center;
}
.two-columns {
    display: flex;
    gap: 40px;
    width: 100%;
    max-width: 1100px;
}
.column {
    flex-basis: calc(50% - 20px);
    text-align: left;
}
.column p {
    font-size: 1em;
    line-height: 1.7;
    color: #333333;
    margin-bottom: 15px;
}
@media (max-width: 768px) {
    .two-columns {
        flex-direction: column;
        gap: 20px;
        align-items: center;
    }
    .column {
        flex-basis: 100%;
        max-width: 500px;
    }
    .pimpa-story h2 {
        font-size: 1.8em;
    }
    #section2 {
         padding: 30px 5%;
    }
}

#section5 {
    background-color: #f0f8ff;
    padding-top: 80px;
    justify-content: center;
    box-sizing: border-box;
}
/* Potentially problematic rule, seems like a typo for section5 or a general partner title */
#section4 h2 {
    font-size: 2.2em;
    font-weight: bold;
    color: #333333;
    margin-bottom: 40px;
    text-align: center;
}
.partner-layout-container {
    display: flex;
    width: 100%;
    max-width: 1200px;
    gap: 20px;
    align-items: stretch;
}
.primary-partners-area {
    flex: 2;
    display: flex;
    gap: 20px;
}
.secondary-partners-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.partner-card {
    background-color: #FFFFFF;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.primary-card {
    flex: 1;
}
.secondary-card {
    /* No specific flex property */
}
.partner-card:hover {
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    transform: translateY(-5px);
}
.partner-card img.partner-logo {
    max-width: 100px;
    height: auto;
    margin-bottom: 15px;
}
.primary-card img.partner-logo {
    max-width: 120px;
}
.secondary-card img.partner-logo {
    max-width: 90px;
}
.partner-card h3.partner-name {
    font-size: 1.3em;
    color: #333333;
    margin-bottom: 10px;
    font-weight: bold;
}
.primary-card h3.partner-name {
    font-size: 1.4em;
}
.secondary-card h3.partner-name {
    font-size: 1.2em;
}
.partner-card p.partner-description {
    font-size: 0.9em;
    color: #555555;
    line-height: 1.5;
    overflow-wrap: break-word;
    hyphens: auto;
    max-height: 100px;
    overflow-y: auto;
}
.primary-card p.partner-description {
    font-size: 0.95em;
}
.secondary-card p.partner-description {
    font-size: 0.85em;
}
@media (max-width: 992px) {
    .partner-layout-container {
        flex-direction: column;
        align-items: center;
        gap: 30px;
    }
    .primary-partners-area,
    .secondary-partners-area {
        flex: none;
        width: 100%;
    }
    .primary-partners-area {
         max-width: 600px;
         flex-direction: column;
    }
    .secondary-partners-area {
        max-width: 450px;
    }
}
@media (max-width: 576px) {
    /* Potentially problematic rule: #section4 h2, likely for partner title */
    #section4 h2 {
        font-size: 1.8em;
        margin-bottom: 30px;
    }
    /* Potentially problematic rule: #section4 padding, likely for #section5 padding */
    #section4 {
        padding: 30px 5%;
    }
    .primary-partners-area,
    .secondary-partners-area {
        gap: 20px;
    }
    .partner-card {
        padding: 15px;
    }
    .partner-card h3.partner-name { font-size: 1.1em; }
    .primary-card h3.partner-name { font-size: 1.2em; }
    .secondary-card h3.partner-name { font-size: 1.0em; }
    .partner-card p.partner-description { font-size: 0.8em; }
    .primary-card p.partner-description { font-size: 0.85em; }
    .secondary-card p.partner-description { font-size: 0.75em; }
}
"""

def extract_css_rules(css_content):
    relevant_rules = []

    section2_keywords = ["#section2", ".pimpa-story", ".two-columns", ".column", ".slide-content-container"]
    section5_keywords = ["#section5", ".partner-layout-container", ".primary-partners-area", ".secondary-partners-area", ".partner-card", ".primary-card", ".secondary-card"]

    general_section_snap_rule = ""
    snap_section_match = re.search(r"(\.snap-container section\s*\{[^}]*\})", css_content, re.IGNORECASE)
    if snap_section_match:
        general_section_snap_rule = snap_section_match.group(1).strip()

    rule_pattern = re.compile(r"([^{]+)\s*\{([^}]*)\}", re.DOTALL)
    media_query_pattern = re.compile(r"(@media[^{]+\{)((?:[^{}]*\{[^{}]*\}[^{}]*|[^{}]+)*)\}", re.DOTALL | re.IGNORECASE)

    non_media_css = re.sub(media_query_pattern, '', css_content)

    for match in rule_pattern.finditer(non_media_css):
        selector = match.group(1).strip()
        properties = match.group(2).strip().replace("\n", "\n    ") # Indent properties

        # Check if selector contains any of the keywords
        # This check is a bit broad, e.g. ".column-something" would match ".column"
        # For more precision, one might use regex word boundaries: fr'\b{keyword}\b'
        if any(keyword in selector for keyword in section2_keywords) or \
           any(keyword in selector for keyword in section5_keywords) or \
           ("section4" in selector and any(kw in selector for kw in ["h2", ".partner", "padding"])): # Heuristic for problematic section4 rules
            relevant_rules.append(f"{selector} {{\n    {properties}\n}}")

    for media_match in media_query_pattern.finditer(css_content):
        media_selector = media_match.group(1).strip()
        media_content_block = media_match.group(2)

        media_specific_rules = []
        for rule_match in rule_pattern.finditer(media_content_block):
            inner_selector = rule_match.group(1).strip()
            inner_properties = rule_match.group(2).strip().replace("\n", "\n        ") # Indent further for @media

            if any(keyword in inner_selector for keyword in section2_keywords) or \
               any(keyword in inner_selector for keyword in section5_keywords) or \
               ("section4" in inner_selector and any(kw in inner_selector for kw in ["h2", ".partner", "padding"])):
                media_specific_rules.append(f"    {inner_selector} {{\n        {inner_properties}\n    }}")

        if media_specific_rules:
            # Strip the opening '{' from media_selector if it's there, as it will be added by f-string
            if media_selector.endswith('{'):
                 media_selector = media_selector[:-1].strip()
            relevant_rules.append(f"{media_selector} {{\n" + "\n".join(media_specific_rules) + "\n}}")

    if general_section_snap_rule:
        is_present = False
        for rule in relevant_rules:
            if general_section_snap_rule.split('{')[0].strip() in rule.split('{')[0].strip():
                is_present = True
                break
        if not is_present:
            relevant_rules.insert(0, general_section_snap_rule)

    return "\n\n".join(relevant_rules)

extracted_css = extract_css_rules(original_index_html_style_content)
print("--- Extracted CSS ---")
print(extracted_css)

problematic_rules_notes = """
Potential Typographical/Misattributed Rules Noted:
1.  `#section4 h2`: Found outside and inside media queries, but seems to style a title for the partner section (which is `#section5`). If there's no actual `#section4 h2` that needs this style, it might be a typo for a class or `#section5 h2`.
2.  `#section4` (padding rule): Found in `@media (max-width: 576px)`, seems intended for `#section5` as it's grouped with partner card responsive styles.
These rules have been extracted if their selectors or context were associated with the partner layout elements, but should be reviewed.
"""
print(problematic_rules_notes)

with open("extracted_relevant_styles.css", "w", encoding="utf-8") as f:
    f.write(extracted_css)
    f.write("\n\n/* --- Notes on problematic rules --- */\n")
    f.write(problematic_rules_notes)

print("Successfully wrote extracted CSS to extracted_relevant_styles.css")
