from typing import Optional

def ufh_heat_output_100(r_value, dT):
    m = 111.8353 * (r_value ** 2) - 39.5733 * r_value + 6.66364
    c = 558.6506 * (r_value ** 2) - 197.8043 * r_value + 33.31581
    return (m * dT) - c

def ufh_heat_output_150(r_value, dT):
    m = 86.6934 * (r_value ** 2) - 31.5422 * r_value + 5.74376
    c = 424.6747 * (r_value ** 2) - 156.4000 * r_value + 28.70193
    return (m * dT) - c

def ufh_heat_output_200(r_value, dT):
    m = 68.2878 * (r_value ** 2) - 25.3673 * r_value + 4.97757
    c = 341.2530 * (r_value ** 2) - 126.7552 * r_value + 24.89369
    return (m * dT) - c

def ufh_heat_output_250(r_value, dT):
    m = 52.8701 * (r_value ** 2) - 20.1915 * r_value + 4.31537
    c = 261.9277 * (r_value ** 2) - 100.4728 * r_value + 21.56901
    return (m * dT) - c

def ufh_heat_output_300(r_value, dT):
    m = 40.9224 * (r_value ** 2) - 16.0253 * r_value + 3.75131
    c = 204.8434 * (r_value ** 2) - 80.0533 * r_value + 18.74228
    return (m * dT) - c

def ufh_heat_output(
    pipe_spacing: int,
    r_value: float,
    dT: Optional[float] = None,
    flow_temp: Optional[float] = None,
    room_temp: Optional[float] = None
) -> float:
    """
    Calculate the heat output in watts per square meter for underfloor heating with a given pipe spacing and R value.

    Args:
        pipe_spacing (int): The spacing of the pipes in millimeters (e.g., 100, 150, 200, 250, 300).
        r_value (float): The total R-value (m²·K/W) of the floor construction above the pipe.
        dT (float, optional): The temperature difference (K or °C) between the average water temperature and the room temperature.
        flow_temp (float, optional): The average water temperature in the pipes (°C). Required if dT is not provided.
        room_temp (float, optional): The room temperature (°C). Required if dT is not provided.

    Returns:
        float: The heat output in watts per square meter (W/m²).
    """
    if dT is None:
        if flow_temp is not None and room_temp is not None:
            dT = flow_temp - room_temp
        else:
            raise ValueError("Must provide either dT or both flow_temp and room_temp")

    if pipe_spacing == 100:
        return ufh_heat_output_100(r_value, dT)
    elif pipe_spacing == 150:
        return ufh_heat_output_150(r_value, dT)
    elif pipe_spacing == 200:
        return ufh_heat_output_200(r_value, dT)
    elif pipe_spacing == 250:
        return ufh_heat_output_250(r_value, dT)
    elif pipe_spacing == 300:
        return ufh_heat_output_300(r_value, dT)
    else:
        raise ValueError(f"Unsupported pipe spacing: {pipe_spacing}. Supported values are: 100, 150, 200, 250, 300")
