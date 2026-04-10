import os
from src.sdlc_system.state.state_file import SDLCState
from src.sdlc_system.utils.utility import Utility


class MarkdownArtifactsNode:
    """
    Graph Node for generating Markdown artifacts for the SDLC process.
    """

    def __init__(self):
        self.utility = Utility()
        self.artifacts_dir = "artifacts"
        os.makedirs(self.artifacts_dir, exist_ok=True)

    # ✅ --- Text Cleaner (Fix Unicode Issues) ---
    def clean_text(self, text):
        if text is None:
            return ""
        if not isinstance(text, str):
            text = str(text)
        return text.encode("utf-8", errors="replace").decode("utf-8")

    # ✅ --- Central File Writer ---
    def write_file(self, filename, content):
        file_path = os.path.join(self.artifacts_dir, filename)
        cleaned_content = self.clean_text(content)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_content)

        return file_path

    # ✅ --- Main Function ---
    def generate_markdown_artifacts(self, state: SDLCState):

        project_name = state.get("project_name", "Project")

        artifacts = {}

        # ------------------ Project Requirements ------------------
        requirements = state.get("requirements", [])
        md_project = f"# Project Requirement for {project_name}\n\n"
        md_project += "## Requirements\n"
        md_project += self.utility.format_list(requirements)

        artifacts["Project_Requirements"] = self.write_file(
            "Project_Requirement.md", md_project
        )

        # ------------------ User Stories ------------------
        user_stories = state.get("user_stories")
        if user_stories:
            md_stories = f"# User Stories for {project_name}\n\n"
            md_stories += self.utility.format_user_stories(user_stories)

            artifacts["User_Stories"] = self.write_file(
                "User_Stories.md", md_stories
            )
        else:
            artifacts["User_Stories"] = None

        # ------------------ Design Documents ------------------
        design_docs = state.get("design_documents")
        if design_docs:
            functional = self.clean_text(
                design_docs.get("functional", "No Functional Design Document available.")
            )
            technical = self.clean_text(
                design_docs.get("technical", "No Technical Design Document available.")
            )

            md_design = f"# Design Documents for {project_name}\n\n"
            md_design += "## Functional Design Document\n"
            md_design += functional
            md_design += "\n\n## Technical Design Document\n"
            md_design += technical

            artifacts["Design_Documents"] = self.write_file(
                "Design_Documents.md", md_design
            )
        else:
            artifacts["Design_Documents"] = None

        # ------------------ Generated Code ------------------
        code_generated = state.get("code_generated")
        if code_generated:
            md_code = f"# Generated Code for {project_name}\n\n"
            md_code += "\n" + code_generated

            artifacts["Generated_Code"] = self.write_file(
                "Generated_Code.md", md_code
            )
        else:
            artifacts["Generated_Code"] = None

        # ------------------ Security Recommendations ------------------
        security_recommendations = state.get("security_recommendations")
        if security_recommendations:
            md_security = f"# Security Recommendations for {project_name}\n\n"
            md_security += security_recommendations

            artifacts["Security_Recommendations"] = self.write_file(
                "Security_Recommendations.md", md_security
            )
        else:
            artifacts["Security_Recommendations"] = None

        # ------------------ Test Cases ------------------
        test_cases = state.get("test_cases")
        if test_cases:
            md_tests = f"# Test Cases for {project_name}\n\n"
            md_tests += "\n" + test_cases

            artifacts["Test_Cases"] = self.write_file(
                "Test_Cases.md", md_tests
            )
        else:
            artifacts["Test_Cases"] = None

        # ------------------ QA Testing Comments ------------------
        qa_testing_comments = state.get("qa_testing_comments")
        if qa_testing_comments:
            md_qa = f"# QA Testing Comments for {project_name}\n\n"
            md_qa += qa_testing_comments

            artifacts["QA_Testing_Comments"] = self.write_file(
                "QA_Testing_Comments.md", md_qa
            )
        else:
            artifacts["QA_Testing_Comments"] = None

        # ------------------ Final State Update ------------------
        state["artifacts"] = artifacts

        return state