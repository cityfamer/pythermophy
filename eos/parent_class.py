from __future__ import division, print_function

class EOS(object):

    # Universal gas constant
    R = 8.3144598 # J/K/mol

    def __init__(self, fluid):
        self.fluid = fluid
        self.molar_mass = fluid.molar_mass
        self.R_sp = self.R/self.molar_mass
        self.ideal_cp_coeffs = fluid.ideal_cp_coeffs

    def get_Z(self, T, p):
        return 1.

    def get_rho(self, T, p, **kwargs):
        if 'Z' in kwargs:
            z = kwargs['Z']
        else:
            z = self.get_Z(T, p)
        #print(z)
        return p/z/self.R_sp/T

    def get_ideal_cp(self, T):
        """
        Get the ideal gas isobaric specific heat capacity (C_p^0) in J/mol/K.
        See http://www.wiley.com/college/moran/CL_0471465704_S/user/tables/TABLE3S/table3sframe.html

        Parameters
        ----------
        T - Temperature [K]

        Returns
        -------
        Ideal gas isobaric specific heat capacity (C_p^0) [J/mol/K].
        """

        cp = 0.
        for i, c_i in enumerate(self.ideal_cp_coeffs):
            cp = cp + c_i*T**i

        # try:
        #     if self.fluid=='CO2':

        #         c = [22.26, 5.981e-2, -3.501e-5, 7.469e-9]
        #         for i, c_i in enumerate(c):
        #             cp = cp + c_i*T**i

        #     else:
        #         raise ValueError('Ideal gas Cp for fluid "{}" not implemented'.format(self.fluid))
        # except ValueError as err:
        #     print(err)

        return cp

    def get_ideal_cv(self, T):
        """
        Get the ideal gas isochoric specific heat capacity (C_v^0) in J/mol/K

        Parameters
        ----------
        T - Temperature [K]

        Returns
        -------
        Ideal gas isochoric specific heat capacity (C_v^0) [J/mol/K]
        """
        return self.get_ideal_cp(T) - self.R

    def get_departure_cp(self, T, p):
        """
        Get the departure (difference between real gas and ideal gas) for isobaric specific heat capacity (C_p) [J/mol/K]

        Parameters
        ----------
        T - Temperature [K]
        p - Pressure [Pa]

        Returns
        -------
        Departure for isobaric specific heat capacity [J/mol/K]
        """
        return 0.

    def get_departure_cv(self, T, p):
        """
        Get the departure (difference between real gas and ideal gas) for isochoric specific heat capacity (C_p) [J/mol/K]

        Parameters
        ----------
        T - Temperature [K]
        p - Pressure [Pa]

        Returns
        -------
        Departure for isochoric specific heat capacity [J/mol/K]
        """
        return 0.

    def get_cp(self, T, p, **kwargs):
        """
        Get the real gas isobaric specific heat capacity (C_p) [J/mol/K]

        Parameters
        ----------
        T - Temperature [K]
        p - Pressure [Pa]

        Returns
        -------
        Real gas isobaric specific heat capacity [J/mol/K]
        """
        return self.get_ideal_cp(T) + self.get_departure_cp(T, p, **kwargs)

    def get_cv(self, T, p, **kwargs):
        """
        Get the real gas isochoric specific heat capacity (C_p) [J/mol/K]

        Parameters
        ----------
        T - Temperature [K]
        p - Pressure [Pa]

        Returns
        -------
        Real gas isochoric specific heat capacity [J/mol/K]
        """
        return self.get_ideal_cv(T) + self.get_departure_cv(T, p, **kwargs)

    def get_adiabatic_index(self, T, p, **kwargs):
        """
        Get the adiabatic index (ratio between isobaric and isochoric heat capacities) for a real gas

        Parameters
        ----------
        T - Temperature [K]
        p - Pressure [Pa]

        Returns
        -------
        Adiabatic index [dimensionless]
        """
        return self.get_cp(T, p, **kwargs)/self.get_cv(T, p, **kwargs)

    def get_speed_of_sound(self, T, p, **kwargs):
        """
        Get the speed of sound in a real gas

        Parameters
        ----------
        T - Temperature [K]
        p - Pressure [Pa]

        Returns
        --------
        Speed of sound [m/s]
        """
        if 'Z' in kwargs:
            z = kwargs['Z']
        else:
            z = self.get_Z(T, p)

        gamma = self.get_adiabatic_index(T, p, **kwargs)
        beta = self.get_isothermal_compressibility(T, p, **kwargs)
        rho = self.get_rho(T, p, **kwargs)

        c = (gamma/beta/rho)**0.5

        return c
