"""
Tests of simulation parameters from
../../covasim/README.md
"""
import unittest

from unittest_support import CovaTest, TProps

TPKeys = TProps.ParKeys.SimKeys
ResKeys = TProps.ResKeys

class SimulationParameterTests(CovaTest):
    def setUp(self):
        super().setUp()
        pass

    def tearDown(self):
        super().tearDown()
        pass

    def test_population_size(self):
        """
        Set population size to vanilla (1234)
        Run sim for one day and check outputs

        Depends on run default simulation
        """
        TPKeys = TProps.ParKeys.SimKeys
        pop_2_one_day = {
            TPKeys.population_scaling_factor: 1,
            TPKeys.number_simulated_days: 1,
            TPKeys.number_agents: 2,
            TPKeys.number_contacts: {'a': 1},
            TPKeys.initial_infected_count: 0
        }
        pop_10_one_day = {
            TPKeys.population_scaling_factor: 1,
            TPKeys.number_simulated_days: 1,
            TPKeys.number_agents: 10,
            TPKeys.number_contacts: {'a': 4},
            TPKeys.initial_infected_count: 0
        }
        pop_123_one_day = {
            TPKeys.population_scaling_factor: 1,
            TPKeys.number_simulated_days: 1,
            TPKeys.number_agents: 123,
            TPKeys.initial_infected_count: 0
        }
        pop_1234_one_day = {
            TPKeys.population_scaling_factor: 1,
            TPKeys.number_simulated_days: 1,
            TPKeys.number_agents: 1234,
            TPKeys.initial_infected_count: 0
        }
        self.run_sim(pop_2_one_day)
        pop_2_pop = self.get_day_zero_ch_value()
        self.run_sim(pop_10_one_day)
        pop_10_pop = self.get_day_zero_ch_value()
        self.run_sim(pop_123_one_day)
        pop_123_pop = self.get_day_zero_ch_value()
        self.run_sim(pop_1234_one_day)
        pop_1234_pop = self.get_day_zero_ch_value()

        self.assertEqual(pop_2_pop, pop_2_one_day[TPKeys.number_agents])
        self.assertEqual(pop_10_pop, pop_10_one_day[TPKeys.number_agents])
        self.assertEqual(pop_123_pop, pop_123_one_day[TPKeys.number_agents])
        self.assertEqual(pop_1234_pop, pop_1234_one_day[TPKeys.number_agents])

        pass

    def test_population_size_ranges(self):
        """
        Intent is to test zero, negative, and excessively large pop sizes
        """
        pop_neg_one_day = {
            TPKeys.population_scaling_factor: 1,
            TPKeys.number_simulated_days: 1,
            TPKeys.number_agents: -10,
            TPKeys.initial_infected_count: 0
        }
        with self.assertRaises(ValueError) as context:
            self.run_sim(pop_neg_one_day)
        error_message = str(context.exception)
        self.assertIn("negative", error_message)

        pop_zero_one_day = {
            TPKeys.population_scaling_factor: 1,
            TPKeys.number_simulated_days: 100,
            TPKeys.number_agents: 0,
            TPKeys.initial_infected_count: 0
        }
        self.run_sim(pop_zero_one_day)
        self.assertEqual(self.simulation_result['results'][ResKeys.susceptible_at_timestep][-1], 0)
        self.assertEqual(self.simulation_result['results'][ResKeys.susceptible_at_timestep][0], 0)

        pass

    def test_population_scaling(self):
        """
        Scale population vanilla (x10) compare
        output people vs parameter defined people

        Depends on population_size
        """
        scale_1_one_day = {
            TPKeys.number_agents: 100,
            TPKeys.population_scaling_factor: 1,
            TPKeys.number_simulated_days: 1
        }
        scale_2_one_day = {
            TPKeys.number_agents: 100,
            TPKeys.population_scaling_factor: 2,
            TPKeys.population_rescaling: False,
            TPKeys.number_simulated_days: 1
        }
        scale_10_one_day = {
            TPKeys.number_agents: 100,
            TPKeys.population_scaling_factor: 10,
            TPKeys.population_rescaling: False,
            TPKeys.number_simulated_days: 1
        }
        self.run_sim(scale_1_one_day)
        scale_1_pop = self.get_day_zero_ch_value()
        self.run_sim(scale_2_one_day)
        scale_2_pop = self.get_day_zero_ch_value()
        self.run_sim(scale_10_one_day)
        scale_10_pop = self.get_day_zero_ch_value()
        self.assertEqual(scale_2_pop, 2 * scale_1_pop)
        self.assertEqual(scale_10_pop, 10 * scale_1_pop)
        pass


    def test_random_seed(self):
        """
        Run two simulations with the same seed
        and one with a different one. Something
        randomly drawn (number of persons infected
        day 2) is identical in the first two and
        different in the third
        """
        self.set_smallpop_hightransmission()
        seed_1_params = {
            TPKeys.random_seed: 1
        }
        seed_2_params = {
            TPKeys.random_seed: 2
        }
        self.run_sim(seed_1_params)
        infectious_seed_1_v1 = self.get_full_result_ch(
            ResKeys.infectious_at_timestep
        )
        exposures_seed_1_v1 = self.get_full_result_ch(
            ResKeys.exposed_at_timestep
        )
        self.run_sim(seed_1_params)
        infectious_seed_1_v2 = self.get_full_result_ch(
            ResKeys.infectious_at_timestep
        )
        exposures_seed_1_v2 = self.get_full_result_ch(
            ResKeys.exposed_at_timestep
        )
        self.assertEqual(infectious_seed_1_v1, infectious_seed_1_v2,
                         msg=f"With random seed the same, these channels should"
                             f"be identical.")
        self.assertEqual(exposures_seed_1_v1, exposures_seed_1_v2,
                         msg=f"With random seed the same, these channels should"
                             f"be identical.")
        self.run_sim(seed_2_params)
        infectious_seed_2 = self.get_full_result_ch(
            ResKeys.infectious_at_timestep
        )
        exposures_seed_2 = self.get_full_result_ch(
            ResKeys.exposed_at_timestep
        )
        self.assertNotEqual(infectious_seed_1_v1, infectious_seed_2,
                         msg=f"With random seed the different, these channels should"
                             f"be distinct.")
        self.assertNotEqual(exposures_seed_1_v1, exposures_seed_2,
                         msg=f"With random seed the different, these channels should"
                             f"be distinct.")
        pass


if __name__ == '__main__':
    unittest.main()
