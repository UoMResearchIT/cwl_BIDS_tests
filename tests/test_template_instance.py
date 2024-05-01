import pytest
import os
import shutil
import tempfile
from dataclasses import dataclass, field
import textwrap

from ..code.template_instance import create_instance

@dataclass
class TemplateTest:
    id: str # test id
    contents: str = ""
    parsed_contents: str = ""
    args: dict = field(default_factory=dict)
    sub: str = "A"
    ses: str = "01"
    name: str = "workflow.yml"
    template: str = "code/workflow.yml.jinja"
    parsed_target: str = "derivatives/sub-A/ses-01/workflow.yml"

    def __post_init__(self):
        args = {
            "sub": self.sub,
            "ses": self.ses,
            "template": self.template
        }
        self.args.update(args)

        self.contents = textwrap.dedent(self.contents)
        self.parsed_contents = textwrap.dedent(self.parsed_contents)

template_tests = [
    TemplateTest("empty"),
    TemplateTest("name", 
                 args = {"name": "foo.bar",
                         "target": "some/other/path/{{name}}"},
                 parsed_target = "some/other/path/foo.bar"),
    TemplateTest("root",
        contents = "{{basedir}}/code/workflow.cwl",
        parsed_contents = "./code/workflow.cwl",
        args = {"target": "{{name}}"},
        parsed_target = "workflow.yml"
    ),
    TemplateTest("yml",
        contents = """
        #!/usr/bin/env cwl-runner
        cwl:tool: {{basedir}}/code/workflow.cwl
        foo: {class: File, path: {{basedir}}/rawdata/{{sub}}/{{ses}}/foo.txt}
        """,
        parsed_contents = """
        #!/usr/bin/env cwl-runner
        cwl:tool: ../../../code/workflow.cwl
        foo: {class: File, path: ../../../rawdata/sub-A/ses-01/foo.txt}
        """
    ),
    TemplateTest("json",
        contents = """
        #!/usr/bin/env cwl-runner
        {
          "cwl:tool": "{{basedir}}/code/workflow.cwl",
          "foo": {"class": "File", "path": "{{basedir}}/rawdata/{{sub}}/{{ses}}/foo.txt"}}
        }
        """,
        parsed_contents = """
        #!/usr/bin/env cwl-runner
        {
          "cwl:tool": "../../../code/workflow.cwl",
          "foo": {"class": "File", "path": "../../../rawdata/sub-A/ses-01/foo.txt"}}
        }
        """,
        template = "code/workflow.json.jinja",
        parsed_target = "derivatives/sub-A/ses-01/workflow.json"
    ),
    TemplateTest("fancy",
        contents = """
        {% macro ses_data() -%}
            {{basedir}}/rawdata/{{sub}}/{{ses}}
        {%- endmacro %}
        file_array:
        {% for j in [1,2,3] %}
          - class: File
            path: {{ses_data()}}/file_{{j}}.txt
        {% endfor %}
        """,
        parsed_contents = """
        file_array:
          - class: File
            path: ../../../rawdata/sub-A/ses-01/file_1.txt
          - class: File
            path: ../../../rawdata/sub-A/ses-01/file_2.txt
          - class: File
            path: ../../../rawdata/sub-A/ses-01/file_3.txt
        """
    )
]

@pytest.fixture(params=template_tests, ids=[t.id for t in template_tests])
def template(request):
    T = request.param

    temp_dir = tempfile.mkdtemp(prefix = T.id + '_')
    os.makedirs(os.path.join(temp_dir, os.path.dirname(T.template)), exist_ok=True)
    with open(os.path.join(temp_dir, T.template), 'w') as f:
        f.write(T.contents)
    yield temp_dir, T
    shutil.rmtree(temp_dir)

def test_create_instance(template):

    temp_dir, T = template

    # Call the function to create an instance
    out_file = create_instance(**T.args, basedir=temp_dir)
    
    assert out_file == os.path.join(temp_dir, T.parsed_target)
    assert os.path.exists(out_file)
    with open(out_file, 'r') as f:
        assert f.read().strip() == T.parsed_contents.strip()