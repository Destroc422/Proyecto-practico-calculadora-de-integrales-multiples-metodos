"""
LaTeX Integral Calculator - Main Entry Point
Professional Scientific Calculator with LaTeX Rendering - Level Wolfram Alpha
Robust version with comprehensive error handling
"""
import logging
import sys
import traceback
import os

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging with UTF-8 encoding
import sys
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler('latex_calculator.log', encoding='utf-8'),
        stream_handler
    ]
)

logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import tkinter
        logger.info(f"+ Tkinter available")
    except ImportError:
        logger.error("- Tkinter not available")
        return False
    
    try:
        import matplotlib
        logger.info(f"+ Matplotlib {matplotlib.__version__} available")
    except ImportError:
        logger.error("- Matplotlib not available")
        return False
    
    try:
        import numpy
        logger.info(f"+ NumPy {numpy.__version__} available")
    except ImportError:
        logger.error("- NumPy not available")
        return False
    
    try:
        import sympy
        logger.info(f"+ SymPy {sympy.__version__} available")
    except ImportError:
        logger.error("- SymPy not available")
        return False
    
    return True


def check_latex_availability():
    """Check if LaTeX rendering is available"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        
        # Try to render a simple LaTeX expression
        fig, ax = plt.subplots(figsize=(1, 1))
        ax.text(0.5, 0.5, r'$\int x^2 dx$', transform=ax.transAxes)
        plt.close(fig)
        
        logger.info("+ LaTeX rendering available")
    except Exception as e:
        logger.warning(f"- LaTeX rendering not available: {str(e)}")
        return False
    
    return True


def main():
    """Main entry point for the LaTeX integral calculator"""
    try:
        logger.info("=" * 50)
        logger.info("Starting LaTeX Integral Calculator - Professional Rendering...")
        logger.info("=" * 50)
        
        # Check dependencies
        if not check_dependencies():
            logger.error("Missing dependencies. Please install:")
            logger.error("pip install sympy matplotlib numpy")
            sys.exit(1)
        
        # Check LaTeX availability
        latex_available = check_latex_availability()
        if not latex_available:
            logger.warning("LaTeX not available - using fallback rendering")
            logger.info("For LaTeX rendering, install:")
            logger.info("  - Windows: MiKTeX, TeX Live, or proTeXt")
            logger.info("  - macOS: MacTeX")
            logger.info("  - Linux: texlive-full")
        
        # Import here to catch import errors early
        from tkinter import Tk
        from ui.professional_main_window import ProfessionalIntegralCalculator
        
        logger.info("+ All imports successful")
        
        # Create main window
        root = Tk()
        root.title("LaTeX Integral Calculator - Professional")
        
        # Configure window
        root.minsize(1400, 800)
        
        # Create LaTeX calculator instance
        logger.info("Creating LaTeX calculator instance...")
        app = ProfessionalIntegralCalculator(root)
        
        logger.info("+ LaTeX calculator created successfully")
        logger.info("+ Application ready")
        logger.info("=" * 50)
        
        # Start the application
        root.mainloop()
        
        logger.info("Application closed normally")
        
    except ImportError as e:
        logger.error(f"Import error: {str(e)}")
        logger.error("Full traceback:")
        logger.error(traceback.format_exc())
        
        print(f"- Error de importacion: {str(e)}")
        print("\n📦 Dependencias requeridas:")
        print("pip install sympy matplotlib numpy")
        print("\n🎨 Para renderizado LaTeX:")
        print("  - Windows: MiKTeX, TeX Live, o proTeXt")
        print("  - macOS: MacTeX")
        print("  - Linux: texlive-full")
        print("\n🔍 Verifica que todos los archivos del proyecto estén presentes:")
        print("  - ui/main_window.py")
        print("  - core/integrator.py")
        print("  - core/parser.py")
        print("  - ui/latex_renderer.py")
        print("  - graph/plotter.py")
        print("  - utils/validators.py")
        print("  - ui/theme_manager.py")
        print("  - data/history_manager.py")
        
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        logger.error("Full traceback:")
        logger.error(traceback.format_exc())
        
        print(f"- Error fatal: {str(e)}")
        print("\n🔍 Esto puede ser causado por:")
        print("  - Archivos corruptos o faltantes")
        print("  - Errores en el codigo")
        print("  - Problemas de configuracion")
        print("\n📋 Revisa el archivo de log: latex_calculator.log")
        
        sys.exit(1)


if __name__ == "__main__":
    main()
