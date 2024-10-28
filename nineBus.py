import pandapower as pp
import pandapower.contingency as contingency
import pprint
import matplotlib.pyplot as mplt
import pandapower.plotting as plt

# Define a function to create the 9-bus network
def create_ieee_9_bus_system():
    # Initialize empty network
    net = pp.create_empty_network()

    # Create buses
    bus1 = pp.create_bus(net, vn_kv=16.5, min_vm_pu=0.95, max_vm_pu=1.05, name="Bus 1")
    bus2 = pp.create_bus(net, vn_kv=18.0, min_vm_pu=0.95, max_vm_pu=1.05, name="Bus 2")
    bus3 = pp.create_bus(net, vn_kv=13.8, min_vm_pu=0.95, max_vm_pu=1.05, name="Bus 3")
    bus4 = pp.create_bus(net, vn_kv=230.0, min_vm_pu=0.95, max_vm_pu=1.05, name="Bus 4")
    bus5 = pp.create_bus(net, vn_kv=230.0, min_vm_pu=0.95, max_vm_pu=1.05, name="Bus 5")
    bus6 = pp.create_bus(net, vn_kv=230.0, min_vm_pu=0.95, max_vm_pu=1.05, name="Bus 6")
    bus7 = pp.create_bus(net, vn_kv=230.0, min_vm_pu=0.95, max_vm_pu=1.05, name="Bus 7")
    bus8 = pp.create_bus(net, vn_kv=230.0, min_vm_pu=0.95, max_vm_pu=1.05,  name="Bus 8")
    bus9 = pp.create_bus(net, vn_kv=230.0, min_vm_pu=0.95, max_vm_pu=1.05,  name="Bus 9")

    # Create generators
    pp.create_gen(net, bus=bus1, sn_mva=247.5,p_mw=0,vm_pu=1.04, min_p_mw=0, max_p_mw=247,max_q_mvar=150,min_q_mvar=-75, controllable=True, name="Gen 1", slack=True)
    pp.create_gen(net, bus=bus2, sn_mva=192.0, p_mw=163, vm_pu=1.025, min_p_mw=60, max_p_mw=163,max_q_mvar=100,min_q_mvar=-50, controllable=True, name="Gen 2")
    pp.create_gen(net, bus=bus3, sn_mva=128, p_mw=85, vm_pu=1.025, min_p_mw=30, max_p_mw=108,max_q_mvar=65,min_q_mvar=-35, controllable=True, name="Gen 3")

    # Create loads
    pp.create_load(net, bus=bus5, p_mw=125.0, q_mvar=50.0, name="Load 1")
    pp.create_load(net, bus=bus6, p_mw=90.0, q_mvar=30.0, name="Load 2")
    pp.create_load(net, bus=bus8, p_mw=100.0, q_mvar=35.0, name="Load 3")

    # Create transformers (between generator and high voltage buses)
    pp.create_transformer_from_parameters(net, hv_bus=bus4, lv_bus=bus1, sn_mva=247.5, vn_hv_kv=230.0,vn_lv_kv=16.5, vk_percent=5.76, vkr_percent=0, pfe_kw=0, i0_percent=0, shift_degree=0,  name="Transformer 1", max_loading_percent=100.0)
    pp.create_transformer_from_parameters(net, hv_bus=bus7, lv_bus=bus2, sn_mva=192.0, vn_hv_kv=230.0,vn_lv_kv=18.0, vk_percent=6.25, vkr_percent=0, pfe_kw=0, i0_percent=0, shift_degree=0, name="Transformer 2", max_loading_percent=100.0)
    pp.create_transformer_from_parameters(net, hv_bus=bus9, lv_bus=bus3, sn_mva=128.0, vn_hv_kv=230.0,vn_lv_kv=13.8, vk_percent=5.86, vkr_percent=0, pfe_kw=0, i0_percent=0, shift_degree=0, name="Transformer 3", max_loading_percent=100.0)

    # Create lines with standard impedance data
    pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus5, length_km=1.0,
                                   r_ohm_per_km=5.29, x_ohm_per_km=44.965, c_nf_per_km=1058.8899, max_i_ka=100.0,
                                   name="Line 4-5", max_loading_percent=100.0)
    pp.create_line_from_parameters(net, from_bus=bus4, to_bus=bus6, length_km=1.0,
                                   r_ohm_per_km=8.993, x_ohm_per_km=48.668,c_nf_per_km=950.59436, max_i_ka=50.0,
                                   name="Line 4-6", max_loading_percent=100.0)
    pp.create_line_from_parameters(net, from_bus=bus5, to_bus=bus7, length_km=1.0,
                                   r_ohm_per_km=16.928, x_ohm_per_km=85.169, c_nf_per_km=1841.0245, max_i_ka=125.0,
                                   name="Line 5-7", max_loading_percent=100.0)
    pp.create_line_from_parameters(net, from_bus=bus6, to_bus=bus9, length_km=1.0,
                                   r_ohm_per_km=20.631, x_ohm_per_km=89.93,c_nf_per_km=2153.8784, max_i_ka=100.0,
                                   name="Line 6-9", max_loading_percent=100.0)
    pp.create_line_from_parameters(net, from_bus=bus7, to_bus=bus8, length_km=1.0,
                                   r_ohm_per_km=4.4965, x_ohm_per_km=38.088, c_nf_per_km=896.44658, max_i_ka=120.0,
                                   name="Line 7-8", max_loading_percent=100.0)
    pp.create_line_from_parameters(net, from_bus=bus8, to_bus=bus9, length_km=1.0,
                                   r_ohm_per_km=6.2951, x_ohm_per_km=53.3232,c_nf_per_km=1257.4318, max_i_ka=50.0,
                                   name="Line 8-9", max_loading_percent=100.0)

    return net


# Function to run power flow analysis
def run_load_flow(net):
    pp.runpp(net, init="flat",algorithm='nr', enforce_q_lims=True, max_iteration=5000)

    print("")
    print("########### Generator data")
    pprint.pp(net.res_gen)

    print("")
    print("########### Line data")
    pprint.pp(net.res_line)

    print("")
    print("########### Bus data")
    pprint.pp(net.res_bus)

    print("")
    print("########### Transformer data")
    pprint.pp(net.res_trafo)

    print("")
    print("########### Load data")
    pprint.pp(net.res_load)


# Function to conduct N-1 contingency analysis
def contingency_analysis(net):
    nminus1_cases = {"line": {"index": net.line.index.values}}
    res = contingency.run_contingency(net, nminus1_cases)
    element_limits = contingency.get_element_limits(net)
    contingency.report_contingency_results(element_limits, res)

    lines = net.line.index
    critical_lines = []
    critical_lines_indx = []

    vmax = 1.05
    vmin = 0.95
    line_loading_max = 100

    for l in lines:
        net.line.loc[l, 'in_service'] = False
        pp.runpp(net, numba=False)
        if net.res_bus.vm_pu.max()>vmax:
            critical_lines.append([l, 'hv'])
            critical_lines_indx.append(l)
        if net.res_bus.vm_pu.min() < vmin:
            critical_lines.append([l, 'lv'])
            critical_lines_indx.append(l)
        if net.res_line.loading_percent.max() > line_loading_max:
            critical_lines.append([l, 'ol'])
            critical_lines_indx.append(l)
        net.line.loc[l, 'in_service'] = True

    fig, ax = mplt.subplots()
    fig.set_figheight(6)
    fig.set_figwidth(8)

    critical_lc = plt.create_line_collection(net, critical_lines_indx, color="r", zorder=2) #create lines

    plt.draw_collections([critical_lc], ax=ax)
    plt.simple_plot(net,  plot_loads=True, plot_gens=True,  ax=ax, show_plot=False)

    mplt.show()

    print("")
    print("########### Contingency Analysis")
    pprint.pp(res)



# Create the IEEE 9-bus system
net = create_ieee_9_bus_system()

# plotting the network
pp.plotting.plotly.simple_plotly(net, respect_switches=True, on_map=False, projection='epsg:4326', map_style='basic', figsize=1.0, aspectratio=(4,3), line_width=1.0, bus_size=10.0, ext_grid_size=20.0, bus_color='blue', line_color='grey', trafo_color='green', trafo3w_color='green', ext_grid_color='yellow', filename='temp-plot.html', auto_open=True, showlegend=True, additional_traces=None)

pp.plotting.to_html(net, 'network.html', respect_switches=True, include_lines=True, include_trafos=True, show_tables=True)

# Run the load flow for the base case
run_load_flow(net)

# Perform (N-1) contingency analysis
print("Perform (N-1) contingency analysis")
contingency_analysis(net)