from openmdao.api import Problem, Group, IndepVarComp, view_model

from six import iteritems
from numpy.testing import assert_almost_equal


def run_test(obj, comp, decimal=3):
    prob = Problem()
    prob.model.add_subsystem('comp', comp)
    prob.setup()

    prob.run_model()
    check = prob.check_partials(compact_print=True)
    for key, subjac in iteritems(check[list(check.keys())[0]]):
        if subjac['magnitude'].fd > 1e-6:
            assert_almost_equal(
                subjac['rel error'].forward, 0., decimal=decimal, err_msg='deriv of %s wrt %s' % key)
            assert_almost_equal(
                subjac['rel error'].reverse, 0., decimal=decimal, err_msg='deriv of %s wrt %s' % key)

def get_default_surfaces():
    wing_dict = {'name' : 'wing',
                 'num_y' : 7,
                 'num_x' : 2,
                 'symmetry' : True,
                 'S_ref_type' : 'wetted',
                 'CL0' : 0.1,
                 'CD0' : 0.1,

                 # Airfoil properties for viscous drag calculation
                 'k_lam' : 0.05,         # percentage of chord with laminar
                                         # flow, used for viscous drag
                 't_over_c' : 0.15,      # thickness over chord ratio (NACA0015)
                 'c_max_t' : .303,       # chordwise location of maximum (NACA0015)
                                         # thickness
                 'with_viscous' : True,  # if true, compute viscous drag

                 # Structural values are based on aluminum 7075
                 'E' : 70.e9,            # [Pa] Young's modulus of the spar
                 'G' : 30.e9,            # [Pa] shear modulus of the spar
                 'yield' : 500.e6 / 2.5, # [Pa] yield stress divided by 2.5 for limiting case
                 'mrho' : 3.e3,          # [kg/m^3] material density
                 'fem_origin' : 0.35,    # normalized chordwise location of the spar
                 't_over_c' : 0.15,      # maximum airfoil thickness
                 'wing_weight_ratio' : 2.,

                 }

    tail_dict = {'name' : 'tail',
                 'num_y' : 5,
                 'num_x' : 3,
                 'symmetry' : False}

    surfaces = [wing_dict, tail_dict]

    return surfaces