#!/usr/bin/env python3
"""
Integration Test Script for Literature Reviewer Multi-Backend Setup

Tests:
1. Backend paths are accessible
2. retrieval_coordinator.py is syntactically correct
3. Backend scripts exist and are executable
4. Sample paper normalization works

Usage:
    python test_integration.py
"""

import json
import sys
from pathlib import Path


class bcolors:
    OK = '\033[92m'
    FAIL = '\033[91m'
    WARN = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    print(f"\n{bcolors.BOLD}{'=' * 60}{bcolors.ENDC}")
    print(f"{bcolors.BOLD}{text}{bcolors.ENDC}")
    print(f"{bcolors.BOLD}{'=' * 60}{bcolors.ENDC}\n")


def print_test(name: str, passed: bool, message: str = ""):
    status = f"{bcolors.OK}✅ PASS{bcolors.ENDC}" if passed else f"{bcolors.FAIL}❌ FAIL{bcolors.ENDC}"
    msg = f" - {message}" if message else ""
    print(f"{status}: {name}{msg}")


def test_backend_paths():
    """Test that all backend skill paths exist."""
    print_header("Test 1: Backend Paths")
    
    base_path = Path(__file__).parent.parent
    all_passed = True
    
    # CNKI Crawler
    cnki_path = base_path.parent / "cnki-crawler"
    cnki_exists = cnki_path.exists()
    print_test("CNKI Crawler path", cnki_exists, str(cnki_path))
    all_passed = all_passed and cnki_exists
    
    if cnki_exists:
        cnki_main = cnki_path / "scripts" / "main.py"
        print_test("  └─ main.py exists", cnki_main.exists())
        all_passed = all_passed and cnki_main.exists()
    
    # OpenAlex (academic-research)
    openalex_path = base_path.parent / "academic-research"
    openalex_exists = openalex_path.exists()
    print_test("OpenAlex (academic-research) path", openalex_exists, str(openalex_path))
    all_passed = all_passed and openalex_exists
    
    if openalex_exists:
        openalex_search = openalex_path / "scripts" / "scholar-search.py"
        print_test("  └─ scholar-search.py exists", openalex_search.exists())
        all_passed = all_passed and openalex_search.exists()
    
    # Google Scholar (academic-research-hub)
    scholar_path = base_path.parent / "academic-research-hub"
    scholar_exists = scholar_path.exists()
    print_test("Google Scholar (academic-research-hub) path", scholar_exists, str(scholar_path))
    all_passed = all_passed and scholar_exists
    
    if scholar_exists:
        scholar_research = scholar_path / "scripts" / "research.py"
        print_test("  └─ research.py exists", scholar_research.exists())
        all_passed = all_passed and scholar_research.exists()
    
    return all_passed


def test_coordinator_script():
    """Test that retrieval_coordinator.py is syntactically correct."""
    print_header("Test 2: Retrieval Coordinator Script")
    
    coordinator_path = Path(__file__).parent / "retrieval_coordinator.py"
    
    if not coordinator_path.exists():
        print_test("retrieval_coordinator.py exists", False)
        return False
    
    print_test("retrieval_coordinator.py exists", True)
    
    # Try to compile the script
    try:
        with open(coordinator_path, "r", encoding="utf-8") as f:
            code = f.read()
        compile(code, str(coordinator_path), "exec")
        print_test("Syntax check", True)
        return True
    except SyntaxError as e:
        print_test("Syntax check", False, f"Line {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print_test("Syntax check", False, str(e))
        return False


def test_models_module():
    """Test that models.py can be imported and Paper class works."""
    print_header("Test 3: Models Module")
    
    models_path = Path(__file__).parent / "models.py"
    
    if not models_path.exists():
        print_test("models.py exists", False)
        return False
    
    print_test("models.py exists", True)
    
    # Try to import and test
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from models import Paper
        
        # Test Paper creation
        paper = Paper(
            id="E1",
            title="Test Paper",
            authors=["Author 1", "Author 2"],
            year=2024,
            source_db="openalex",
            backend="academic-research"
        )
        
        print_test("Paper class instantiation", True)
        
        # Test to_dict
        paper_dict = paper.to_dict()
        print_test("Paper.to_dict()", True)
        
        # Test from_dict
        paper2 = Paper.from_dict(paper_dict)
        print_test("Paper.from_dict()", True)
        
        return True
        
    except Exception as e:
        print_test("Models import/test", False, str(e))
        return False


def test_normalization():
    """Test paper normalization functions."""
    print_header("Test 4: Paper Normalization")
    
    coordinator_path = Path(__file__).parent / "retrieval_coordinator.py"
    
    if not coordinator_path.exists():
        print_test("retrieval_coordinator.py exists", False)
        return False
    
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from retrieval_coordinator import RetrievalCoordinator
        
        # Create a mock coordinator for testing
        coordinator = RetrievalCoordinator(output_dir="/tmp/test")
        
        # Test OpenAlex normalization
        openalex_sample = {
            "title": "Test Paper",
            "authorships": [
                {"author": {"display_name": "Author 1"}},
                {"author": {"display_name": "Author 2"}}
            ],
            "primary_location": {
                "source": {"display_name": "Test Journal"}
            },
            "abstract": "Test abstract",
            "publication_year": 2024,
            "doi": "10.1234/test",
            "url": "https://example.com",
            "cited_by_count": 10,
            "open_access": {"url": "https://open.example.com"}
        }
        
        normalized = coordinator._normalize_openalex_paper(openalex_sample)
        if normalized:
            print_test("OpenAlex normalization", True)
            print_test("  └─ Has source_db", normalized.get("source_db") == "openalex")
            print_test("  └─ Has backend", normalized.get("backend") == "academic-research")
            print_test("  └─ Has authors", len(normalized.get("authors", [])) == 2)
        else:
            print_test("OpenAlex normalization", False, "Returned None")
            return False
        
        # Test Google Scholar normalization
        scholar_sample = {
            "title": "Test Paper",
            "authors": ["Author 1", "Author 2"],
            "year": 2024,
            "venue": "Test Conference",
            "snippet": "Test snippet",
            "url": "https://example.com",
            "citations": 15
        }
        
        normalized = coordinator._normalize_scholar_paper(scholar_sample)
        if normalized:
            print_test("Google Scholar normalization", True)
            print_test("  └─ Has source_db", normalized.get("source_db") == "google_scholar")
            print_test("  └─ Has backend", normalized.get("backend") == "academic-research-hub")
            print_test("  └─ Has authors", len(normalized.get("authors", [])) == 2)
        else:
            print_test("Google Scholar normalization", False, "Returned None")
            return False
        
        return True
        
    except Exception as e:
        print_test("Normalization test", False, str(e))
        import traceback
        traceback.print_exc()
        return False


def test_search_backends_doc():
    """Test that search-backends.md exists and has required sections."""
    print_header("Test 5: Documentation")
    
    backends_doc = Path(__file__).parent.parent / "references" / "search-backends.md"
    
    if not backends_doc.exists():
        print_test("search-backends.md exists", False)
        return False
    
    print_test("search-backends.md exists", True)
    
    try:
        with open(backends_doc, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check for required sections
        required_sections = [
            "Backend Selection Matrix",
            "CNKI Backend",
            "OpenAlex Backend",
            "Google Scholar Backend",
            "Normalized Paper Schema",
        ]
        
        all_present = True
        for section in required_sections:
            present = section in content
            print_test(f"  └─ Section: {section}", present)
            all_present = all_present and present
        
        return all_present
        
    except Exception as e:
        print_test("Documentation check", False, str(e))
        return False


def main():
    print(f"\n{bcolors.BOLD}🧪 Literature Reviewer - Multi-Backend Integration Tests{bcolors.ENDC}\n")
    
    results = []
    
    results.append(("Backend Paths", test_backend_paths()))
    results.append(("Coordinator Script", test_coordinator_script()))
    results.append(("Models Module", test_models_module()))
    results.append(("Paper Normalization", test_normalization()))
    results.append(("Documentation", test_search_backends_doc()))
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{bcolors.OK}✅{bcolors.ENDC}" if result else f"{bcolors.FAIL}❌{bcolors.ENDC}"
        print(f"{status} {name}")
    
    print(f"\n{bcolors.BOLD}Total: {passed}/{total} tests passed{bcolors.ENDC}")
    
    if passed == total:
        print(f"\n{bcolors.OK}🎉 All tests passed! Integration is ready.{bcolors.ENDC}\n")
        return 0
    else:
        print(f"\n{bcolors.FAIL}⚠️  Some tests failed. Please review the errors above.{bcolors.ENDC}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
