def prompt(
    role: str,
    task: str,
    context: str,
    constraints: str,
    output_format: str,
    examples: str
) -> str:
    """
    Combines prompt components using standard string formatting.
    """
    # 1. Define the main structure with placeholders
    full_template = """
    {role_content}
    {context_content}
    {task_content}                                    
    {constraints_content}                                         
    {output_format_content}                                          
    {examples_content} 
    """

    # 2. Inject the components into the structure
    # We use .strip() to clean up any accidental leading/trailing whitespace
    return full_template.format(
        role_content=role.strip(),
        context_content=context.strip(),
        task_content=task.strip(),
        constraints_content=constraints.strip(),
        output_format_content=output_format.strip(),
        examples_content=examples.strip()
    )