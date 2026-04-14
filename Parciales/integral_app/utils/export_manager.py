"""
Enhanced Export Manager for Professional Calculator
Advanced export capabilities with multiple formats and quality options
"""
import matplotlib.pyplot as plt
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any, Union
import os
import json
from datetime import datetime
import base64
from io import BytesIO, StringIO

logger = logging.getLogger(__name__)


class ExportManager:
    """Advanced export manager with multiple format support"""
    
    def __init__(self):
        """Initialize export manager"""
        self.export_history = []
        self.default_settings = {
            'dpi': 300,
            'quality': 95,
            'transparent': False,
            'bbox_inches': 'tight',
            'facecolor': 'white',
            'edgecolor': 'none',
            'pad_inches': 0.1
        }
        
        # Supported formats
        self.image_formats = ['png', 'jpg', 'jpeg', 'svg', 'pdf', 'eps', 'tiff', 'bmp']
        self.data_formats = ['json', 'csv', 'txt', 'xlsx', 'xml']
        self.report_formats = ['html', 'pdf', 'latex', 'markdown']
    
    def export_plot(self, figure, filepath: str, format_type: str = 'png', 
                   settings: Optional[Dict] = None, metadata: Optional[Dict] = None) -> Dict:
        """
        Export plot with advanced options
        
        Args:
            figure: Matplotlib figure to export
            filepath: Output file path
            format_type: Export format
            settings: Export settings
            metadata: Additional metadata to include
            
        Returns:
            Dict with export results
        """
        try:
            # Merge settings
            export_settings = {**self.default_settings, **(settings or {})}
            
            # Validate format
            format_type = format_type.lower().lstrip('.')
            if format_type not in self.image_formats:
                raise ValueError(f"Unsupported format: {format_type}")
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Prepare export parameters
            export_params = self._prepare_export_params(format_type, export_settings)
            
            # Export the figure
            start_time = datetime.now()
            figure.savefig(filepath, format=format_type, **export_params)
            end_time = datetime.now()
            
            # Get file info
            file_info = self._get_file_info(filepath)
            
            # Create export record
            export_record = {
                'filepath': filepath,
                'format': format_type,
                'settings': export_settings,
                'metadata': metadata or {},
                'timestamp': start_time.isoformat(),
                'duration': (end_time - start_time).total_seconds(),
                'file_info': file_info,
                'success': True
            }
            
            # Add to history
            self.export_history.append(export_record)
            
            logger.info(f"Plot exported successfully: {filepath} ({format_type})")
            return export_record
            
        except Exception as e:
            logger.error(f"Error exporting plot: {str(e)}")
            
            error_record = {
                'filepath': filepath,
                'format': format_type,
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'success': False
            }
            
            self.export_history.append(error_record)
            return error_record
    
    def export_data(self, data: Dict, filepath: str, format_type: str = 'json') -> Dict:
        """
        Export calculation data in various formats
        
        Args:
            data: Data to export (calculation results, steps, etc.)
            filepath: Output file path
            format_type: Export format
            
        Returns:
            Dict with export results
        """
        try:
            format_type = format_type.lower().lstrip('.')
            if format_type not in self.data_formats:
                raise ValueError(f"Unsupported data format: {format_type}")
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            start_time = datetime.now()
            
            if format_type == 'json':
                self._export_json(data, filepath)
            elif format_type == 'csv':
                self._export_csv(data, filepath)
            elif format_type == 'txt':
                self._export_txt(data, filepath)
            elif format_type == 'xlsx':
                self._export_xlsx(data, filepath)
            elif format_type == 'xml':
                self._export_xml(data, filepath)
            
            end_time = datetime.now()
            
            # Get file info
            file_info = self._get_file_info(filepath)
            
            export_record = {
                'filepath': filepath,
                'format': format_type,
                'type': 'data',
                'timestamp': start_time.isoformat(),
                'duration': (end_time - start_time).total_seconds(),
                'file_info': file_info,
                'success': True
            }
            
            self.export_history.append(export_record)
            logger.info(f"Data exported successfully: {filepath} ({format_type})")
            
            return export_record
            
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return {
                'filepath': filepath,
                'format': format_type,
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'success': False
            }
    
    def export_report(self, content: Dict, filepath: str, format_type: str = 'html') -> Dict:
        """
        Export comprehensive report
        
        Args:
            content: Report content (analysis, results, plots)
            filepath: Output file path
            format_type: Export format
            
        Returns:
            Dict with export results
        """
        try:
            format_type = format_type.lower().lstrip('.')
            if format_type not in self.report_formats:
                raise ValueError(f"Unsupported report format: {format_type}")
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            start_time = datetime.now()
            
            if format_type == 'html':
                self._export_html_report(content, filepath)
            elif format_type == 'pdf':
                self._export_pdf_report(content, filepath)
            elif format_type == 'latex':
                self._export_latex_report(content, filepath)
            elif format_type == 'markdown':
                self._export_markdown_report(content, filepath)
            
            end_time = datetime.now()
            
            # Get file info
            file_info = self._get_file_info(filepath)
            
            export_record = {
                'filepath': filepath,
                'format': format_type,
                'type': 'report',
                'timestamp': start_time.isoformat(),
                'duration': (end_time - start_time).total_seconds(),
                'file_info': file_info,
                'success': True
            }
            
            self.export_history.append(export_record)
            logger.info(f"Report exported successfully: {filepath} ({format_type})")
            
            return export_record
            
        except Exception as e:
            logger.error(f"Error exporting report: {str(e)}")
            return {
                'filepath': filepath,
                'format': format_type,
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'success': False
            }
    
    def export_batch(self, items: List[Dict], output_dir: str) -> Dict:
        """
        Export multiple items in batch
        
        Args:
            items: List of export items with type, data, format, etc.
            output_dir: Output directory
            
        Returns:
            Dict with batch export results
        """
        try:
            results = []
            success_count = 0
            error_count = 0
            
            for i, item in enumerate(items):
                try:
                    item_type = item.get('type', 'plot')
                    format_type = item.get('format', 'png')
                    
                    # Generate filename
                    base_name = item.get('filename', f'item_{i+1}')
                    filename = f"{base_name}.{format_type}"
                    filepath = os.path.join(output_dir, filename)
                    
                    if item_type == 'plot':
                        result = self.export_plot(item['data'], filepath, format_type, 
                                                 item.get('settings'), item.get('metadata'))
                    elif item_type == 'data':
                        result = self.export_data(item['data'], filepath, format_type)
                    elif item_type == 'report':
                        result = self.export_report(item['data'], filepath, format_type)
                    else:
                        raise ValueError(f"Unknown item type: {item_type}")
                    
                    results.append(result)
                    
                    if result['success']:
                        success_count += 1
                    else:
                        error_count += 1
                        
                except Exception as e:
                    error_record = {
                        'item_index': i,
                        'error': str(e),
                        'success': False
                    }
                    results.append(error_record)
                    error_count += 1
            
            batch_result = {
                'output_dir': output_dir,
                'total_items': len(items),
                'success_count': success_count,
                'error_count': error_count,
                'results': results,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Batch export completed: {success_count}/{len(items)} successful")
            return batch_result
            
        except Exception as e:
            logger.error(f"Error in batch export: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'success': False
            }
    
    def export_to_base64(self, figure, format_type: str = 'png', 
                         settings: Optional[Dict] = None) -> Dict:
        """
        Export plot to base64 string for web use
        
        Args:
            figure: Matplotlib figure
            format_type: Export format
            settings: Export settings
            
        Returns:
            Dict with base64 data
        """
        try:
            # Merge settings
            export_settings = {**self.default_settings, **(settings or {})}
            
            # Create buffer
            buffer = BytesIO()
            
            # Prepare export parameters
            export_params = self._prepare_export_params(format_type, export_settings)
            
            # Save to buffer
            figure.savefig(buffer, format=format_type, **export_params)
            buffer.seek(0)
            
            # Convert to base64
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # Create data URI
            data_uri = f"data:image/{format_type};base64,{image_base64}"
            
            result = {
                'base64': image_base64,
                'data_uri': data_uri,
                'format': format_type,
                'size_bytes': len(image_base64),
                'success': True
            }
            
            buffer.close()
            logger.info(f"Plot exported to base64 ({format_type})")
            return result
            
        except Exception as e:
            logger.error(f"Error exporting to base64: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }
    
    def _prepare_export_params(self, format_type: str, settings: Dict) -> Dict:
        """Prepare export parameters based on format"""
        params = settings.copy()
        
        # Format-specific adjustments
        if format_type in ['jpg', 'jpeg']:
            params['transparent'] = False  # JPEG doesn't support transparency
            if 'quality' not in params:
                params['quality'] = 95
        elif format_type == 'png':
            if 'transparent' not in params:
                params['transparent'] = False
        elif format_type == 'svg':
            # SVG doesn't use DPI
            params.pop('dpi', None)
        elif format_type == 'pdf':
            if 'transparent' not in params:
                params['transparent'] = False
        
        return params
    
    def _get_file_info(self, filepath: str) -> Dict:
        """Get file information"""
        try:
            stat = os.stat(filepath)
            return {
                'size_bytes': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'exists': True
            }
        except Exception as e:
            return {
                'error': str(e),
                'exists': False
            }
    
    def _export_json(self, data: Dict, filepath: str):
        """Export data as JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    def _export_csv(self, data: Dict, filepath: str):
        """Export data as CSV"""
        import csv
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write headers
            if isinstance(data, dict):
                headers = list(data.keys())
                writer.writerow(headers)
                
                # Write values
                values = []
                for key in headers:
                    value = data[key]
                    if isinstance(value, (list, tuple)):
                        values.append(str(value))
                    else:
                        values.append(str(value))
                writer.writerow(values)
    
    def _export_txt(self, data: Dict, filepath: str):
        """Export data as plain text"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("Calculation Results Export\n")
            f.write("=" * 50 + "\n\n")
            
            for key, value in data.items():
                f.write(f"{key}:\n")
                if isinstance(value, (list, tuple)):
                    for item in value:
                        f.write(f"  - {item}\n")
                else:
                    f.write(f"  {value}\n")
                f.write("\n")
    
    def _export_xlsx(self, data: Dict, filepath: str):
        """Export data as Excel (basic implementation)"""
        try:
            import pandas as pd
            
            # Convert to DataFrame
            if isinstance(data, dict):
                df = pd.DataFrame([data])
            else:
                df = pd.DataFrame(data)
            
            # Export to Excel
            df.to_excel(filepath, index=False)
            
        except ImportError:
            # Fallback to CSV if pandas not available
            logger.warning("pandas not available, exporting as CSV instead")
            self._export_csv(data, filepath.replace('.xlsx', '.csv'))
    
    def _export_xml(self, data: Dict, filepath: str):
        """Export data as XML"""
        def dict_to_xml(d, root_name='root'):
            xml = f'<{root_name}>\n'
            for key, value in d.items():
                xml += f'  <{key}>{value}</{key}>\n'
            xml += f'</{root_name}>'
            return xml
        
        xml_content = dict_to_xml(data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(xml_content)
    
    def _export_html_report(self, content: Dict, filepath: str):
        """Export report as HTML"""
        html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe de Cálculo Integral</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }}
        .section {{ margin: 20px 0; }}
        .math {{ font-family: 'Times New Roman', serif; font-style: italic; }}
        .result {{ background-color: #f5f5f5; padding: 10px; border-left: 4px solid #2196F3; }}
        table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Informe de Cálculo Integral</h1>
        <p>Generado: {timestamp}</p>
    </div>
    
    {content}
    
    <div class="footer">
        <p><em>Generado por Calculadora de Integrales Pro v4.0</em></p>
    </div>
</body>
</html>
        """
        
        # Generate HTML content
        html_content = ""
        
        if 'function' in content:
            html_content += f'<div class="section"><h2>Función</h2><div class="math">{content["function"]}</div></div>'
        
        if 'result' in content:
            html_content += f'<div class="section"><h2>Resultado</h2><div class="result">{content["result"]}</div></div>'
        
        if 'steps' in content:
            html_content += '<div class="section"><h2>Pasos del Cálculo</h2><ol>'
            for step in content['steps']:
                html_content += f'<li>{step}</li>'
            html_content += '</ol></div>'
        
        if 'analysis' in content:
            html_content += '<div class="section"><h2>Análisis</h2>'
            for key, value in content['analysis'].items():
                html_content += f'<p><strong>{key}:</strong> {value}</p>'
            html_content += '</div>'
        
        # Fill template
        final_html = html_template.format(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            content=html_content
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_html)
    
    def _export_pdf_report(self, content: Dict, filepath: str):
        """Export report as PDF (basic implementation)"""
        try:
            # Try to use reportlab
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch
            
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title = Paragraph("Informe de Cálculo Integral", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Content
            for key, value in content.items():
                heading = Paragraph(key.capitalize(), styles['Heading2'])
                story.append(heading)
                
                if isinstance(value, (list, tuple)):
                    for item in value:
                        text = Paragraph(str(item), styles['Normal'])
                        story.append(text)
                else:
                    text = Paragraph(str(value), styles['Normal'])
                    story.append(text)
                
                story.append(Spacer(1, 12))
            
            # Build PDF
            doc.build(story)
            
        except ImportError:
            # Fallback to HTML if reportlab not available
            logger.warning("reportlab not available, exporting as HTML instead")
            self._export_html_report(content, filepath.replace('.pdf', '.html'))
    
    def _export_latex_report(self, content: Dict, filepath: str):
        """Export report as LaTeX"""
        latex_template = r"""
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{geometry}
\geometry{a4paper, margin=1in}

\title{Informe de Cálculo Integral}
\author{Calculadora de Integrales Pro v4.0}
\date{\timestamp}

\begin{document}

\maketitle

{content}

\end{document}
        """
        
        # Generate LaTeX content
        latex_content = ""
        
        if 'function' in content:
            latex_content += f"\\section{{Función}}\n\\[\n{content['function']}\n\\]\n\n"
        
        if 'result' in content:
            latex_content += f"\\section{{Resultado}}\n\\[\n{content['result']}\n\\]\n\n"
        
        if 'steps' in content:
            latex_content += "\\section{Pasos del Cálculo}\n\\begin{enumerate}\n"
            for step in content['steps']:
                latex_content += f"\\item {step}\n"
            latex_content += "\\end{enumerate}\n\n"
        
        # Fill template
        final_latex = latex_template.format(
            timestamp=datetime.now().strftime('%Y-%m-%d'),
            content=latex_content
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_latex)
    
    def _export_markdown_report(self, content: Dict, filepath: str):
        """Export report as Markdown"""
        markdown_content = f"# Informe de Cálculo Integral\n\n"
        markdown_content += f"**Generado:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if 'function' in content:
            markdown_content += f"## Función\n\n```\n{content['function']}\n```\n\n"
        
        if 'result' in content:
            markdown_content += f"## Resultado\n\n```\n{content['result']}\n```\n\n"
        
        if 'steps' in content:
            markdown_content += "## Pasos del Cálculo\n\n"
            for i, step in enumerate(content['steps'], 1):
                markdown_content += f"{i}. {step}\n"
            markdown_content += "\n"
        
        if 'analysis' in content:
            markdown_content += "## Análisis\n\n"
            for key, value in content['analysis'].items():
                markdown_content += f"**{key}:** {value}\n\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    
    def get_export_history(self) -> List[Dict]:
        """Get export history"""
        return self.export_history.copy()
    
    def clear_export_history(self):
        """Clear export history"""
        self.export_history.clear()
        logger.info("Export history cleared")
    
    def get_supported_formats(self, export_type: str = 'all') -> List[str]:
        """Get supported formats for given export type"""
        if export_type == 'image':
            return self.image_formats
        elif export_type == 'data':
            return self.data_formats
        elif export_type == 'report':
            return self.report_formats
        else:
            return list(set(self.image_formats + self.data_formats + self.report_formats))
    
    def validate_export_path(self, filepath: str, format_type: str) -> Dict:
        """Validate export path and format"""
        result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check format
        format_type = format_type.lower().lstrip('.')
        if format_type not in self.get_supported_formats():
            result['valid'] = False
            result['errors'].append(f"Unsupported format: {format_type}")
        
        # Check directory
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                result['warnings'].append(f"Created directory: {directory}")
            except Exception as e:
                result['valid'] = False
                result['errors'].append(f"Cannot create directory: {str(e)}")
        
        # Check file permissions
        if os.path.exists(filepath):
            if not os.access(filepath, os.W_OK):
                result['valid'] = False
                result['errors'].append(f"File is not writable: {filepath}")
        
        return result


# Create singleton instance
export_manager = ExportManager()
