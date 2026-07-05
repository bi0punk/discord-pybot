import os
import subprocess


def test_readme_exists():
    assert os.path.isfile("README.md")


def test_gitignore_exists():
    assert os.path.isfile(".gitignore")


def test_images_not_tracked():
    result = subprocess.run(
        ["git", "ls-files", "img/"],
        capture_output=True, text=True
    )
    assert result.stdout.strip() == "", f"Images still tracked: {result.stdout.strip()}"
