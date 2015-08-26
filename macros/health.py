__author__ = 'p017058'


def gen_status_frag(hpcurr_prop="HPC",
                    hpmax_prop="HPM",
                    con_prop="Constitution",
                    wound1_state="Wounded x1",
                    wound2_state="Wounded x2",
                    wound3_state="Wounded x3",
                    disabled_state="Disabled",
                    dying_state="Dying",
                    dead_state="Dead"):
    """
    Add macro block to automatically handle change Health "States".
    :return:
    """
    code = '\n'
    code += '\n[h: setState("%s", 0)] ' % wound1_state
    code += '\n[h: setState("%s", 0)] ' % wound2_state
    code += '\n[h: setState("%s", 0)] ' % wound3_state
    code += '\n[h: setState("%s", 0)] ' % disabled_state
    code += '\n[h: setState("%s", 0)] ' % dying_state

    data = {'HPC': hpcurr_prop, 'HPM': hpmax_prop, 'con': con_prop, 'state': wound1_state}
    code += '\n[h, if(%(HPC)s <= %(HPM)s*0.75 && %(HPC)s > %(HPM)s*0.50): setState("%(state)s", 1)]' % data

    data['state'] = wound2_state
    code += '\n[h, if(%(HPC)s <= %(HPM)s*0.50 && %(HPC)s > %(HPM)s*0.25): setState("%(state)s", 1)]' % data

    data['state'] = wound3_state
    code += '\n[h, if(%(HPC)s <= %(HPM)s*0.25 && %(HPC)s > %(HPM)s*0.00): setState("%(state)s", 1)]' % data

    data['state'] = disabled_state
    code += '\n[h, if(%(HPC)s <= 0 && %(HPC)s >= -%(con)s) : setState("%(state)s", 1)]' % data

    data['state'] = dying_state
    code += '\n[h, if(%(HPC)s <  0 && %(HPC)s >= -%(con)s) : setState("%(state)s", 1)]' % data

    data['state'] = dead_state
    code += '\n[h, if(%(HPC)s < -%(con)s): setState("%(state)s", 1)]' % data

    return code
