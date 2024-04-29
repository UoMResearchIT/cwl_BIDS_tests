import pytest
import os
import shutil
import tempfile

from ..code.template_instance import create_instance

@pytest.fixture()
def template():

    template = """
#!/usr/bin/env cwl-runner
cwl:tool: code/workflow.cwl
foo: {class: File, path: rawdata/{{sub}}/{{ses}}/foo.txt}
"""
    sub = "A"
    ses = "01"
    name = "workflow"

    instance = """
#!/usr/bin/env cwl-runner
cwl:tool: code/workflow.cwl
foo: {class: File, path: rawdata/sub-A/ses-01/foo.txt}
"""
    template_file = os.path.join("code", name + ".yml")

    temp_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(temp_dir, os.path.dirname(template_file)), exist_ok=False)

    with open(os.path.join(temp_dir, template_file), 'w') as f:
        f.write(template)
    
    yield temp_dir, template_file, sub, ses, name, instance
    shutil.rmtree(temp_dir)

def test_create_instance(template):

    temp_dir, template_file, sub, ses, name, instance = template

    # Call the function to create an instance
    out_file = create_instance(template_file, sub, ses, basedir = temp_dir)
    assert out_file == os.path.join("derivatives", "sub-" + sub, name, name + ".yml")
    assert os.path.exists(out_file)
    with open(out_file, 'r') as f:
        assert f.read().strip() == instance.strip()