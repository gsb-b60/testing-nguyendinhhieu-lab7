import unittest
from unittest.mock import patch

import gps_service

from yummy_app import YummyApp


# ================================================================
# CAP DO 1: Bo test co ban cho san ( Moi chi dat ~35% Coverage )
# ================================================================

class TestEasyLevel(unittest.TestCase):
    # Kiem thu chuc nang co ban tinh tien don hang
    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {" pho ": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {" pho ": 1, " bun ": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {" pho ": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)


# ================================================================
# CAP DO 2 ( TIET 3): Kiem thu ma khuyen mai
# ================================================================

class TestMediumLevel(unittest.TestCase):
    def test_apply_giam10_online_valid(self):
        app = YummyApp(network_status="online")

        self.assertEqual(app.apply_promo_code(100000, "GIAM10"), 90000)

    def test_apply_giam10_offline_raises_connection_error(self):
        app = YummyApp(network_status="offline")

        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_apply_new_os_only_on_os_15(self):
        app = YummyApp(os_version=15)

        self.assertEqual(app.apply_promo_code(100000, "NEW_OS_ONLY"), 80000)

    def test_apply_new_os_only_on_os_14_raises_value_error(self):
        app = YummyApp(os_version=14)

        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")


# ================================================================
# CAP DO 3: Kiem thu goi dich vu GPS bang mock
# ================================================================

class TestHardLevel(unittest.TestCase):
    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_is_in_area(self, mock_get_location):
        mock_get_location.return_value = (10.0, 105.0)

        restaurants = YummyApp().get_nearby_restaurants()

        self.assertEqual(
            restaurants,
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
        )
        mock_get_location.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_is_outside_area(
        self, mock_get_location
    ):
        mock_get_location.return_value = (20.0, 110.0)

        restaurants = YummyApp().get_nearby_restaurants()

        self.assertEqual(restaurants, [])
        mock_get_location.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_signal_lost(
        self, mock_get_location
    ):
        mock_get_location.side_effect = gps_service.GPSSignalLostError

        restaurants = YummyApp().get_nearby_restaurants()

        self.assertEqual(restaurants, "Khong the xac dinh vi tri.")
        mock_get_location.assert_called_once_with()

if __name__ == "__main__":
    unittest.main()