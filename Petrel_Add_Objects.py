#### SMOOTH WELL LOG ####

# Start: PWR Description

# https://docs.prizm.cegal-geo.com/products/PrizmWorkflowRunner/PythonAPI/cegalprizm.pycoderunner.WorkflowDescription.html

from cegalprizm.pycoderunner import WorkflowDescription, DomainObjectsEnum
from cegalprizm.pycoderunner import *
from cegalprizm.pycoderunner import WorkflowDescription, DomainObjectsEnum, MeasurementNamesEnum, TemplateNamesEnum
from cegalprizm.pycoderunner import WorkflowDescription, DomainObjectsEnum, MeasurementNamesEnum

####  WORKFLOW DESCRIPTION ####
# The class WorkflowDescription is used to define the Cegal Prizm workflow. It is assigned to a Python variable called 'pwr_description'
pwr_description = WorkflowDescription(name="Smooth well log",
                                      category="Demo: Python operations - Wells",
                                      description="The script applies a rolling filter to smooth a well log, using a specified window size to determine the range of data points considered for each smoothing operation. This is a simple Cegal Prizm worklfow demonstrating the deployment of Python code to Petrel users and how you can expand Petrel functionality with additional algorithms.",
                                      authors="author@company",
                                      version="1.0")

pwr_description = WorkflowDescription(name="Vsh Calculator",
                                      category="Demo: Python operations - Wells",
                                      description="Calculate Vsh using different algorithms",
                                      authors="author@company",
                                      version="1.0")

vel_description='''This Cegal Prizm workflows applies a velocity anisotropy correction on deviated wells. The input log for Vp and Vs must be the brine saturated case.'''
pwr_description = WorkflowDescription(name="Velocity anisotropy",
                                      category="Demo: Python operations - Wells",
                                      description=vel_description,
                                      authors="author@company.com",
                                      version="1.0")

pwr_description = WorkflowDescription(name="Despike logs",
                                      category="Petrophysics",
                                      description="Simple approach to remove outliers in your log data.\n  Despiking based on difference between the rolling median and the rolling std deviation.",
                                      authors="author@company",
                                      version="0.1")



# Use the variable pwr_description to define the UI in the Prizm Workflow Runner and let the Petrel user select the input data.
# This creates a Python dictionary 'parameters' with the GUID and/or values of the user's input data.

####### SELECT A WELL ########
pwr_description.add_object_ref_parameter(name="well_id", # input_well
                                        label="Well",    # Select Well
                                        description="Select well", 
                                        object_type=DomainObjectsEnum.Well  #eg well_id = 10/4-1
                                        )

#### SELECT LOG(S) ######

pwr_description.add_object_ref_parameter(name="log_id", 
                                        label="Log", 
                                        description="The (continuous) well log to be smoothed", 
                                        object_type=DomainObjectsEnum.WellContinuousLog,
                                        linked_input_name="well_id"                 ## LINKED 
                                        )
pwr_description.add_object_ref_parameter(name="log_id", 
                                         label="Select logs:", 
                                         description="A continuous welllog",
                                         object_type=DomainObjectsEnum.WellContinuousLog, 
                                         linked_input_name="well_id"
                                         select_multiple=True                       ## MULTIPLE
                                         )
pwr_description.add_object_ref_parameter(name="log_id", 
                                        label="Gamma ray input log",
                                        description="Gamma ray log used to calculate Vshale", 
                                        object_type=DomainObjectsEnum.WellContinuousLog, 
                                        template_type='GammaRay',                   ## TEMPLATE
                                        #template_type=TemplateNamesEnum.GammaRay,  # [i for i in TemplateNamesEnum][0:]
                                        linked_input_name="well_id"
                                        )
pwr_description.add_object_ref_parameter(name='vp',
                                         label='VP log (Brine saturated case)',
                                         description='Select a vp log',
                                         object_type=DomainObjectsEnum.WellContinuousLog,
                                         linked_input_name='input_well',
                                         template_type='P-velocity',        # S-velocity, Porosity - effective, Vshale, Density
                                         measurement_type='m/s'                     ## MEASUREMENT
                                         )
pwr_description.add_object_ref_parameter(name='vs',
                                         label='VS log (Brine saturated case)',
                                         description='Select a vs log',
                                         object_type=DomainObjectsEnum.WellContinuousLog,
                                         linked_input_name='input_well',
                                         template_type='S-velocity',
                                         measurement_type='m/s'
                                         )
pwr_description.add_object_ref_parameter(name='survey',
                                         label='Well survey',
                                         description='Select a well survey',
                                         object_type=DomainObjectsEnum.WellSurvey,  ## WELL SURVEY
                                         linked_input_name='input_well'
                                         )
pwr_description.add_object_ref_parameter(name="gwl_id",                             ## GLOBAL WELL LOG
                                        label= "Target Vsh global well log", 
                                        description="Select the global well log the calculated Vshale should be written to", 
                                        object_type=DomainObjectsEnum.GlobalLogContinuous, 
                                        template_type='VShale'
                                        )

# dict values are scipy.signal.windows
smoothing_list={0:"barthann",1:"bartlett",2:"blackman",3:"bohman",4:"boxcar",5:"hann",6:"cosine",7:"nuttall",8:"exponential",9:"flattop",10:"hamming",11:"parzen",12:"taylor",13:"triang",14:"tukey",15:"gaussian"}
pwr_description.add_enum_parameter(name="algorithm_smooth",
                                        label="Select the smoothing algorithm",
                                        description="List of available algorithms. This is a selection of window types in scipy.signal.windows",
                                        options=smoothing_list,  # list provided above
                                        default_value=15         # gaussian
                                        )
pwr_description.add_enum_parameter(name='methods',
                                        label='Select method:',
                                        description='Choose which method you want to use for calculation Vsh',
                                        options={0:'Linear',1:'Larionov - tertiary rocks',2:'Larionov - older rocks',3:'Clavier',4:'Stieber'}
                                        )
pwr_description.add_integer_parameter(name="window_length", 
                                        label="Window Length", 
                                        description="The window length to be used when smoothing", 
                                        default_value=80, 
                                        minimum_value=2, 
                                        maximum_value=500
                                        )
pwr_description.add_integer_parameter(name='grs_input',
                                        label='Clean rock GR value:',
                                        description='The GammaRay value associated with a clean reservoir having no shale ',
                                        default_value=30, 
                                        minimum_value=1, 
                                        maximum_value=1000
                                        )
pwr_description.add_integer_parameter(name='grsh_input',
                                        label='Shale GammaRay value',
                                        description='The GammaRay value associated with a zone of 100% shale',
                                        default_value=130, 
                                        minimum_value=1, 
                                        maximum_value=1000
                                        )
pwr_description.add_string_parameter(name="suffix", 
                                        label="Suffix", 
                                        description="The suffix to be appended to the name of the smoothed log", 
                                        default_value="smooth"
                                        )
pwr_description.add_boolean_parameter(name="overwrite_vsh",
                                        label="Overwrite if Vsh log exist",
                                        description="Decide if existing vsh log should be overwritten",
                                        default_value=False
                                        )
#### HORIZON OBJECTS 
pwr_description.add_object_ref_parameter(name='horizon',
                                         label='Select a seismic horizon',
                                         description='Select a seismic horizon',
                                         object_type=DomainObjectsEnum.HorizonInterpretation
                                         )
pwr_description.add_object_ref_parameter(name='horizon_interpretation',
                                         label='Select interpretation',
                                         description='Select the  interpretation associated to the selected horizon',
                                         object_type=DomainObjectsEnum.HorizonInterpretation3D,
                                         linked_input_name='horizon'
                                         )

# End: PWR Description



# Start: PWR Description

from cegalprizm.pycoderunner import WorkflowDescription,DomainObjectsEnum,MeasurementNamesEnum,TemplateNamesEnum

pwr_description = WorkflowDescription(name="Horizon - outliers correction",
                                      category="Seismic interpretation",
                                      description="Use this workflow to remove the outliers in your horizon interpretation",
                                      authors="author@company",
                                      version="1.0")

pwr_description.add_integer_parameter(name='size',label='Define the moving window size',description='Using a moving window we compute the  local mean and standard deviation for each point in the horizon array.',default_value=40, minimum_value=2, maximum_value=1000)
pwr_description.add_float_parameter(name='threshold',label='Define threshold value',description='A point is considered an outlier if its difference from the local mean is greater than threshold times the local standard deviation. The threshold determines how strict or lenient the outlier detection is.',default_value=1, minimum_value=0, maximum_value=1000)
pwr_description.add_integer_parameter(name='nws',label='Define the neighborhood size',description='The identified outliers are corrected by replacing them with a weighted average of their neighbors. The neighborhood size for calculating the weighted average is defined by the indices in the slicing operation.\nNote that choice of the neighborhood window size (6x6 in this case) and its positioning relative to the outlier can affect the correction result. Adjusting these parameters might provide different outcomes depending on the specific characteristics of the data and the desired correction behavior.',default_value=10, minimum_value=2, maximum_value=1000)
pwr_description.add_integer_parameter(name='iterations',label='Define the number of iterations',description='The approach is to iteratively identify and correct outliers until a specified number of iterations are reached.\nWhy iteratively? Seismic horizons can have various scales of irregularities. Some might be genuine features, while others could be due to noise or inaccuracies in the interpretation process. By performing the correction iteratively, the approach tries to address both large-scale and fine-scale outliers, refining the horizon in each pass.',default_value=3, minimum_value=1, maximum_value=1000)

# End: PWR Description