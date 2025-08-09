# (这里的代码和我们上次在“代码执行”节点中使用的核心逻辑一样)
# (它接收JSON，返回一个文件名:文件内容的字典)
import json

def convert_json_to_md_files(json_data):
    if not isinstance(json_data, list):
        return {"error": "Input data is not a valid JSON array."}

    markdown_files = {}
    for event_data in json_data:
        original_filename = event_data.get("original_filename")
        if not original_filename: continue
        
        full_content = event_data.get("full_content", "")
        references = event_data.get("zotero_references", [])
        md_content_to_write = full_content
        if references:
            md_content_to_write += "\\n\\n"
            for ref in references:
                citation_text = ref.get("citation_text")
                if citation_text:
                    md_content_to_write += f"{citation_text}\\n"
        markdown_files[original_filename] = md_content_to_write
    return markdown_files