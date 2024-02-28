import re
from textwrap import dedent as dedent_text
import hyperdiv as hd


def parse_doc(doc):
    chunks = []
    current_chunk = None
    lines = dedent_text(doc).split("\n")

    inside_string = False

    def process_current_chunk():
        if current_chunk and current_chunk["content"]:
            chunks.append(current_chunk)

    for line in lines:
        stripped = line.strip()
        if inside_string:
            if '"""' in stripped or "'''" in stripped:
                inside_string = False
        else:
            if '"""' in stripped or "'''" in stripped:
                inside_string = True

            if stripped.startswith("```py-nodemo"):
                process_current_chunk()
                current_chunk = dict(type="code-nodemo", content="")
                continue
            elif stripped.startswith("```py"):
                process_current_chunk()
                current_chunk = dict(type="code", content="")
                continue
            elif (
                line.strip().startswith("```")
                and current_chunk
                and current_chunk["type"] in ("code", "code-nodemo")
            ):
                process_current_chunk()
                current_chunk = dict(type="text", content="")
                continue
        if not current_chunk:
            current_chunk = dict(type="text", content="")
        current_chunk["content"] += line + "\n"

    process_current_chunk()

    return chunks


def code_example(code, code_to_execute=None):
    state = hd.state(error=None)
    if code_to_execute is None:
        code_to_execute = code
    with hd.hbox(wrap="wrap", border="1px solid neutral-50", border_radius="large"):
        with hd.box(horizontal_scroll=False, grow=1, basis=0, min_width=18):
            hd.code(code, height="100%")
        with hd.box(grow=1, basis=0, min_width=18):
            with hd.box(padding=1, gap=1):
                if state.error:
                    hd.text(f"Error: {state.error}", font_color="red")
                    if hd.button("Reset", size="small").clicked:
                        state.error = None
                else:
                    try:
                        exec(dedent_text(code_to_execute), globals(), globals())
                    except Exception as e:
                        state.error = str(e)


def render_doc_chunks(doc_chunks):
    with hd.box(gap=1.5):
        for i, doc_chunk in enumerate(doc_chunks):
            with hd.scope(i):
                if doc_chunk["content"].strip() == "":
                    continue
                if doc_chunk["type"] == "text":
                    component_pattern = r"@component\((\w+)\)"
                    component_replacement = r"[`\1`](/reference/components/\1)"

                    prop_type_pattern = r"@prop_type\((\w+)\)"
                    prop_type_replacement = r"[`\1`](/reference/prop-types/\1)"

                    design_token_pattern = r"@design_token\((\w+)\)"
                    design_token_replacement = r"[`\1`](/reference/design-tokens/\1)"

                    new_text = re.sub(
                        component_pattern, component_replacement, doc_chunk["content"]
                    )
                    new_text = re.sub(
                        prop_type_pattern, prop_type_replacement, new_text
                    )
                    new_text = re.sub(
                        design_token_pattern, design_token_replacement, new_text
                    )
                    hd.markdown(new_text)
                elif doc_chunk["type"] == "code-nodemo":
                    hd.code(doc_chunk["content"])
                else:
                    code_example(doc_chunk["content"])


def docs_markdown(doc):
    return render_doc_chunks(parse_doc(doc))
