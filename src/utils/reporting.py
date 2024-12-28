import json
import os
from datetime import datetime
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class TestReport:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        self.results: List[Dict] = []
        self.start_time = datetime.now()
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Ensure the output directory exists"""
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            os.makedirs(os.path.join(self.output_dir, "screenshots"), exist_ok=True)
        except Exception as e:
            logger.error(f"Error creating output directories: {e}")
    
    def add_result(self, step: str, status: str, details: str = "", screenshot: str = None):
        """Add a test result"""
        self.results.append({
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "status": status,
            "details": details,
            "screenshot": screenshot
        })
    
    def save_screenshot(self, page, name: str) -> str:
        """Save a screenshot and return its path"""
        try:
            filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = os.path.join(self.output_dir, "screenshots", filename)
            page.screenshot(path=path)
            return path
        except Exception as e:
            logger.error(f"Error saving screenshot: {e}")
            return ""
    
    def generate_report(self):
        """Generate HTML test report"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        success_count = sum(1 for r in self.results if r["status"] == "success")
        failure_count = sum(1 for r in self.results if r["status"] == "failure")
        
        html = self._generate_html_report(
            success_count, failure_count, duration
        )
        
        try:
            report_path = os.path.join(self.output_dir, "report.html")
            with open(report_path, "w") as f:
                f.write(html)
            logger.info(f"Report generated: {report_path}")
        except Exception as e:
            logger.error(f"Error generating report: {e}")
    
    def _generate_html_report(self, success_count: int, failure_count: int, duration: float) -> str:
        """Generate HTML content for the report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Automation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .success {{ color: green; }}
                .failure {{ color: red; }}
                .result {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; }}
                .screenshot {{ max-width: 800px; }}
            </style>
        </head>
        <body>
            <h1>Test Automation Report</h1>
            <div class="summary">
                <p>Start Time: {self.start_time}</p>
                <p>Duration: {duration:.2f} seconds</p>
                <p>Success: <span class="success">{success_count}</span></p>
                <p>Failures: <span class="failure">{failure_count}</span></p>
            </div>
            <h2>Test Steps</h2>
        """
        
        for result in self.results:
            html += f"""
            <div class="result">
                <h3>{result["step"]}</h3>
                <p>Status: <span class="{result["status"]}">{result["status"]}</span></p>
                <p>Time: {result["timestamp"]}</p>
                <p>Details: {result["details"]}</p>
            """
            if result["screenshot"]:
                html += f'<img class="screenshot" src="{result["screenshot"]}" alt="Step Screenshot">'
            html += "</div>"
        
        html += """
        </body>
        </html>
        """
        return html