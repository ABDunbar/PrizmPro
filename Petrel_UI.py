#### SMOOTH WELL LOG ####

# Start: PWR Description

from cegalprizm.pycoderunner import WorkflowDescription, DomainObjectsEnum

# dict values are scipy.signal.windows
smoothing_list = {
    0: "barthann",
    1: "bartlett",
    2: "blackman",
    3: "bohman",
    4: "boxcar",
    5: "hann",
    6: "cosine",
    7: "nuttall",
    8: "exponential",
    9: "flattop",
    10: "hamming",
    11: "parzen",
    12: "taylor",
    13: "triang",
    14: "tukey",
    15: "gaussian",
}

# The class WorkflowDescription is used to define the Cegal Prizm workflow. It is assigned to a Python variable called 'pwr_description'
pwr_description = WorkflowDescription(
    name="Smooth well log",
    category="Demo: Python operations - Wells",
    description="The script applies a rolling filter to smooth a well log, using a specified window size to determine the range of data points considered for each smoothing operation. This is a simple Cegal Prizm worklfow demonstrating the deployment of Python code to Petrel users and how you can expand Petrel functionality with additional algorithms.",
    authors="author@company",
    version="1.0",
)

# Use the variable pwr_description to define the UI in the Prizm Workflow Runner and let the Petrel user select the input data.
# This creates a Python dictionary 'parameters' with the GUID and/or values of the user's input data.

pwr_description.add_object_ref_parameter(
    name="well_id",
    label="Well",
    description="Select well",
    object_type=DomainObjectsEnum.Well,  # eg well_id = 10/4-1
)

pwr_description.add_object_ref_parameter(
    name="log_id",
    label="Log",
    description="The well log to be smoothed",
    object_type=DomainObjectsEnum.WellContinuousLog,  # eg log_id = GR
    linked_input_name="well_id",
)

pwr_description.add_enum_parameter(
    name="algorithm_smooth",
    label="Select the smoothing algorithm",
    description="List of available algorithms. This is a selection of window types in scipy.signal.windows",
    options=smoothing_list,  # list provided above
    default_value=15,  # gaussian
)

pwr_description.add_integer_parameter(
    name="window_length",
    label="Window Length",
    description="The window length to be used when smoothing",
    default_value=80,
    minimum_value=2,
    maximum_value=500,
)

pwr_description.add_string_parameter(
    name="suffix",
    label="Suffix",
    description="The suffix to be appended to the name of the smoothed log",
    default_value="smooth",
)
# End: PWR Description

from cegalprizm.pythontool import PetrelConnection, Well, WellLog

ptp = PetrelConnection()
print("PetrelConnection established")

petrel_objects = ptp.get_petrelobjects_by_guids(
    [parameters["well_id"], parameters["log_id"]]
)

# Extract the well object from the retrieved objects and check if it's valid
well = petrel_objects[0]
if not isinstance(well, Well) == True:
    raise AssertionError("No well selected")

print("Selected well passed to Cegal Prizm workflow")

# Extract the continuous log object from the retrieved objects and check if it's valid
cont_log = petrel_objects[1]
if not isinstance(cont_log, WellLog) == True:
    raise AssertionError("No well log selected")

print("Selected well log passed to Cegal Prizm workflow")


################################## END SMOOTH WELL LOG ########################


#### CALCULATING VSHALE ####

# Start: PWR Description

from cegalprizm.pycoderunner import *

# The class WorkflowDescription is used to define the Cegal Prizm workflow. It is assigned to a Python variable called 'pwr_description'
pwr_description = WorkflowDescription(
    name="Vsh Calculator",
    category="Demo: Python operations - Wells",
    description="Calculate Vsh using different algorithms",
    authors="author@company",
    version="1.0",
)

# Use the variable pwr_description to define the UI in the Prizm Workflow Runner and let the Petrel user select the input data.
# This creates a Python dictionary 'parameters' with the GUID and/or values of the user's input data.

pwr_description.add_object_ref_parameter(
    name="well_id",
    label="Select well",
    description="Select the well",
    object_type=DomainObjectsEnum.Well,
)
pwr_description.add_object_ref_parameter(
    name="log_id",
    label="Gamma ray input log",
    description="Gamma ray log used to calculate Vshale",
    object_type=DomainObjectsEnum.WellContinuousLog,
    template_type="GammaRay",
    linked_input_name="well_id",
)
pwr_description.add_object_ref_parameter(
    name="gwl_id",
    label="Target Vsh global well log",
    description="Select the global well log the calculated Vshale should be written to",
    object_type=DomainObjectsEnum.GlobalLogContinuous,
    template_type="VShale",
)
pwr_description.add_boolean_parameter(
    name="overwrite_vsh",
    label="Overwrite if Vsh log exist",
    description="Decide if existing vsh log should be overwritten",
    default_value=False,
)
pwr_description.add_integer_parameter(
    name="grs_input",
    label="Clean rock GR value:",
    description="The GammaRay value associated with a clean reservoir having no shale ",
    default_value=30,
    minimum_value=1,
    maximum_value=1000,
)
pwr_description.add_integer_parameter(
    name="grsh_input",
    label="Shale GammaRay value",
    description="The GammaRay value associated with a zone of 100% shale",
    default_value=130,
    minimum_value=1,
    maximum_value=1000,
)
pwr_description.add_enum_parameter(
    name="methods",
    label="Select method:",
    description="Choose which method you want to use for calculation Vsh",
    options={
        0: "Linear",
        1: "Larionov - tertiary rocks",
        2: "Larionov - older rocks",
        3: "Clavier",
        4: "Stieber",
    },
)
# End: PWR Description

print("Establishing PetrelConnection")

from cegalprizm.pythontool import PetrelConnection, Well, WellLog, GlobalWellLog

ptp = PetrelConnection()

print("PetrelConnection established")

# Retrieve the selected well using its GUID and check if it's a valid Well object
user_well = ptp.get_petrelobjects_by_guids([parameters["well_id"]])[0]
if not isinstance(user_well, Well) == True:
    raise AssertionError("No well selected")

print("Retrieved well by guid")

# Retrieve the selected gamma ray log using its GUID and check if it's a valid WellLog object
gr_log = ptp.get_petrelobjects_by_guids([parameters["log_id"]])[0]
if not isinstance(gr_log, WellLog) == True:
    raise AssertionError("No gamma ray log selected as input")

print("Retrieved gamma ray input log by guid")

# Retrieve the selected Vshale global well log using its GUID and check if it's a valid GlobalWellLog object
target_gwl = ptp.get_petrelobjects_by_guids([parameters["gwl_id"]])[0]
if not isinstance(target_gwl, GlobalWellLog) == True:
    raise AssertionError("No vshale global well log selected as target log")
print("Retrieved target vshale global well log by guid")

# Check if the Vshale log already exists in the well and set the overwrite flag accordingly
try:
    existing_log = target_gwl.log(user_well.petrel_name)
    print("Target log does exist in well. Values will be overwritten.")
    overwrite_log = True
except:
    print("Target log does not exist in well. New log will be created.")
    overwrite_log = False
    pass

petrel_overwrite = parameters["overwrite_vsh"]

# Raise an exception if the user chose not to overwrite the Vshale but the log already exists
if petrel_overwrite == False and overwrite_log == True:
    raise Exception("Log already exist,but overwrite is set to False")

# Retrieve the selected method and input values for the Vsh calculation
method = parameters["methods"]
GRS_input = parameters["grs_input"]
GRSh_input = parameters["grsh_input"]

################################## END CALCULATING VSHALE ########################

#### VELOCITY ANISOTROPY ####

# Start: PWR Description

from cegalprizm.pycoderunner import (
    WorkflowDescription,
    DomainObjectsEnum,
    MeasurementNamesEnum,
    TemplateNamesEnum,
)

vel_description = """This Cegal Prizm workflows applies a velocity anisotropy correction on deviated wells. The input log for Vp and Vs must be the brine saturated case."""

pwr_description = WorkflowDescription(
    name="Velocity anisotropy",
    category="Demo: Python operations - Wells",
    description=vel_description,
    authors="author@company.com",
    version="1.0",
)

# Use the variable pwr_description to define the UI in the Prizm Workflow Runner and let the Petrel user select the input data.
# This creates a Python dictionary 'parameters' with the GUID and/or values of the user's input data.

pwr_description.add_object_ref_parameter(
    name="input_well",
    label="Well",
    description="Select a well",
    object_type=DomainObjectsEnum.Well,
)
pwr_description.add_object_ref_parameter(
    name="vp",
    label="VP log (Brine saturated case)",
    description="Select a vp log",
    object_type=DomainObjectsEnum.WellContinuousLog,
    linked_input_name="input_well",
    template_type="P-velocity",
    measurement_type="m/s",
)
pwr_description.add_object_ref_parameter(
    name="vs",
    label="VS log (Brine saturated case)",
    description="Select a vs log",
    object_type=DomainObjectsEnum.WellContinuousLog,
    linked_input_name="input_well",
    template_type="S-velocity",
    measurement_type="m/s",
)
pwr_description.add_object_ref_parameter(
    name="phi",
    label="PHIE log",
    description="Select a porosity-effective log",
    object_type=DomainObjectsEnum.WellContinuousLog,
    linked_input_name="input_well",
    template_type="Porosity - effective",
)
pwr_description.add_object_ref_parameter(
    name="vsh",
    label="Vsh log",
    description="Select a Vshale log",
    object_type=DomainObjectsEnum.WellContinuousLog,
    linked_input_name="input_well",
    template_type="VShale",
)
pwr_description.add_object_ref_parameter(
    name="rho",
    label="Rho log (Brine saturated case)",
    description="Select a Density log",
    object_type=DomainObjectsEnum.WellContinuousLog,
    linked_input_name="input_well",
    template_type="Density",
)
pwr_description.add_object_ref_parameter(
    name="survey",
    label="Well survey",
    description="Select a well survey",
    object_type=DomainObjectsEnum.WellSurvey,
    linked_input_name="input_well",
)


# End: PWR Description

import numpy as np
import pandas as pd


from cegalprizm.pythontool import (
    PetrelConnection,
    GlobalWellLog,
    Well,
    WellLog,
    WellSurvey,
)

ptp = PetrelConnection(allow_experimental=True)
print("Connected to {}".format(ptp.get_current_project_name()))

petrel_objects = ptp.get_petrelobjects_by_guids(
    [
        parameters["input_well"],
        parameters["vp"],
        parameters["vs"],
        parameters["phi"],
        parameters["vsh"],
        parameters["rho"],
        parameters["survey"],
    ]
)

well = petrel_objects[0]
if not isinstance(well, Well) == True:
    raise AssertionError("No well selected")

vp = petrel_objects[1]
if not isinstance(vp, WellLog) == True:
    raise AssertionError("No Vp log selected")

vs = petrel_objects[2]
if not isinstance(vs, WellLog) == True:
    raise AssertionError("No Vs log selected")

phi = petrel_objects[3]
if not isinstance(phi, WellLog) == True:
    raise AssertionError("No porosity log selected")

vshale = petrel_objects[4]
if not isinstance(vshale, WellLog) == True:
    raise AssertionError("No VShale log selected")

rho = petrel_objects[5]
if not isinstance(rho, WellLog) == True:
    raise AssertionError("No density log selected")

survey = petrel_objects[6]
if not isinstance(survey, WellSurvey) == True:
    raise AssertionError("No well survey log selected")

log_list = [vp, vs, phi, vshale, rho]

print("All inputs are passed to the Cegal Prizm workflow")

############################ END VELOCITY ANISOTROPY #######################################

#### LOG DESPIKING ####


# Start: PWR Description

from cegalprizm.pycoderunner import (
    WorkflowDescription,
    DomainObjectsEnum,
    MeasurementNamesEnum,
)

# The class WorkflowDescription is used to define the Cegal Prizm workflow. It is assigned to a Python variable called 'pwr_description'
pwr_description = WorkflowDescription(
    name="Despike logs",
    category="Petrophysics",
    description="Simple approach to remove outliers in your log data.\n  Despiking based on difference between the rolling median and the rolling std deviation.",
    authors="author@company",
    version="0.1",
)

# Use the variable pwr_description to define the UI in the Prizm Workflow Runner and let the Petrel user select the input data.
# This creates a Python dictionary 'parameters' with the GUID and/or values of the user's input data.

pwr_description.add_integer_parameter(
    name="int_value",
    label="Window size: ",
    description="An integer input",
    default_value=5,
    minimum_value=2,
    maximum_value=100,
)
pwr_description.add_object_ref_parameter(
    name="log_id",
    label="Select logs:",
    description="A continuous welllog",
    object_type=DomainObjectsEnum.WellContinuousLog,
    select_multiple=True,
)
pwr_description.add_boolean_parameter(
    name="overwrite",
    label="Overwrite existing logs?",
    description="Choose if you want to overwrite the existing logs or create new ones",
    default_value=False,
)

# End: PWR Description

from cegalprizm.pythontool import *

petrel = PetrelConnection(allow_experimental=True)

# Retrieve the user defined window size and assign it to a variable
window_size = parameters["int_value"]

# Retrieve the user defined value of the boolean parameter
overwrite_logs = parameters["overwrite"]

# Initialize a list to store the user selected logs
nested_logs = []

for el in parameters["log_id"]:
    nested_logs.append(petrel.get_petrelobjects_by_guids([el]))

# Check if no logs are selected and raise an error if true
if len(nested_logs) == 0:
    raise ValueError("No wells have been selected")

# Check if any selected logs are invalid and raise an error if true
if any(item is None for item in nested_logs):
    raise ValueError("Some selected wells are not valid")

################################# END LOG DESPIKING #####################################
