import importlib
import os

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

def load_nodes():
    current_dir = os.path.dirname(__file__)
    nodes_dir = os.path.join(current_dir, 'nodes')  # Pfad zum 'nodes'-Unterordner
    for filename in os.listdir(nodes_dir):
        if filename.endswith(".py") and filename != "__init__.py" and filename != "CustomDatatypes.py":
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f".nodes.{module_name}", package=__name__)
                if hasattr(module, "NODE_CLASS_MAPPINGS"):
                    NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
                if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
                    NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
            except Exception as e:
                print(f"Error loading module {module_name}: {e}")

load_nodes()

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]


print("""

                        .#####,                                                 
                      #########                                                 
                    (########     .################(                            
                   #######(    ########################.                        
                 .#######    ##########*       ##########(                      
                 ######(   ########.               ########                     
                #######   #######.   ,###########    #######                    
                ######   ,######    ###############   #######                   
               (######   #######   #######  .######    ######                   
               (######   #######   /#####    ######   .######                   
                ######.   #######          /#######   #######                   
                #######    ##########(/##########(   #######                    
                 ########    ###################    #######                     
                  ,########     ############,     ########                      
                    ##########                .#########,                       
                      /###############################                          
                         ,#########################                             
                              *###############                                  

                                  BV Nodes

""")


