from typing import Any
from pydantic import validate_call

from ..client import ClientABC, APIResponse


class FirewallMixin(ClientABC):
    """mixin class for firewall functions"""

    def apply_firewall_changes(self) -> APIResponse:
        """Apply pending firewall changes. This will reload all filter items. This endpoint returns no data.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-apply-firewall"""
        url = "/api/v1/firewall/apply"
        method = "POST"
        return self.call(url=url, method=method)

    def create_firewall_nat_one_to_one(self, **args: dict[str, Any]) -> APIResponse:
        """Add a new NAT 1:1 Mapping.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-nat-1-to-1-mappings"""
        method = "POST"
        url = "/api/v1/firewall/nat/one_to_one"
        return self.call(url=url, method=method, payload=args)

    def delete_firewall_nat_one_to_one(self, **args: dict[str, Any]) -> APIResponse:
        """Delete a NAT 1:1 Mapping.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-nat-1-to-1-mappings"""
        method = "DELETE"
        url = "/api/v1/firewall/nat/one_to_one"
        return self.call(url=url, method=method, payload=args)

    def update_firewall_nat_one_to_one(self, **args: dict[str, Any]) -> APIResponse:
        """Update a NAT 1:1 Mapping.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#4-update-nat-1-to-1-mappings"""
        method = "PUT"
        url = "/api/v1/firewall/nat/one_to_one"
        return self.call(url=url, method=method, payload=args)

    def get_firewall_nat_one_to_one(self, **kwargs: dict[str, Any]) -> APIResponse:
        """Read 1:1 NAT mappings. https://github.com/jaredhendrickson13/pfsense-api#3-read-nat-1-to-1-mappings"""
        url = "/api/v1/firewall/nat/one_to_one"
        return self.call(url=url, payload=kwargs)

    def update_nat_outbound_settings(self, **args: dict[str, Any]) -> APIResponse:
        """Update outbound NAT mode settings.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-update-outbound-nat-settings"""
        method = "PUT"
        url = "/api/v1/firewall/nat/outbound"
        return self.call(url=url, method=method, payload=args)

    def create_outbound_nat_mapping(self, **args: dict[str, Any]) -> APIResponse:
        """Create new outbound NAT mappings.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-outbound-nat-mappings"""
        method = "POST"
        url = "/api/v1/firewall/nat/outbound/mapping"
        return self.call(url=url, method=method, payload=args)

    def delete_outbound_nat_mapping(self, **args: dict[str, Any]) -> APIResponse:
        """Delete outbound NAT mappings.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-outbound-nat-mappings"""
        method = "DELETE"
        url = "/api/v1/firewall/nat/outbound/mapping"
        return self.call(url=url, method=method, payload=args)

    def get_nat_outbound_mapping(self, **kwargs: dict[str, Any]) -> APIResponse:
        """Read existing outbound NAT mode mappings.
        https://github.com/jaredhendrickson13/pfsense-api#3-read-outbound-nat-mappings"""
        url = "/api/v1/firewall/nat/outbound/mapping"
        return self.call(url=url, payload=kwargs)

    def update_outbound_nat_mapping(self, **args: dict[str, Any]) -> APIResponse:
        """Update existing outbound NAT mappings.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#4-update-outbound-nat-mappings"""
        method = "PUT"
        url = "/api/v1/firewall/nat/outbound/mapping"
        return self.call(url=url, method=method, payload=args)

    def create_nat_port_forward(self, **args: dict[str, Any]) -> APIResponse:
        """Add a new NAT port forward rule.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-nat-port-forwards"""
        url = "/api/v1/firewall/nat/port_forward"
        method = "POST"
        return self.call(url=url, method=method, payload=args)

    def delete_nat_port_forward(self, **args: dict[str, Any]) -> APIResponse:
        """Delete a NAT port forward rule.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-nat-port-forwards"""
        url = "/api/v1/firewall/nat/port_forward"
        method = "DELETE"
        return self.call(url=url, method=method, payload=args)

    def get_firewall_nat_port_forward(self, **kwargs: dict[str, Any]) -> APIResponse:
        """Read NAT port forward rules. https://github.com/jaredhendrickson13/pfsense-api#3-read-nat-port-forwards"""
        url = "/api/v1/firewall/nat/port_forward"
        return self.call(url=url, payload=kwargs)

    def update_nat_port_forward(self, **args: dict[str, Any]) -> APIResponse:
        """Update a NAT port forward rule.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#4-update-nat-port-forwards"""
        method = "PUT"
        url = "/api/v1/firewall/nat/port_forward"
        return self.call(url=url, method=method, payload=args)

    def delete_all_firewall_rules(self) -> APIResponse:
        """Deletes all existing firewall rules. Useful for scripts setting up firewall rules from scratch.
        Note: this endpoint will not reload the firewall filter automatically, you must make another API call
        to the /api/v1/firewall/apply endpoint. Ensure firewall rules are created before reloading the filter
        to prevent lockout!
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-delete-all-firewall-rules"""
        url = "/api/v1/firewall/rule/flush"
        method = "DELETE"
        return self.call(url=url, method=method)

    def create_firewall_schedule(self, **args: dict[str, Any]) -> APIResponse:
        """Add a firewall schedule.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-schedule"""
        url = "/api/v1/firewall/schedule"
        method = "POST"
        return self.call(url=url, method=method, payload=args)

    def delete_firewall_schedule(self, **args: dict[str, Any]) -> APIResponse:
        """Delete a firewall schedule.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-schedule"""
        method = "DELETE"
        url = "/api/v1/firewall/schedule"
        return self.call(url=url, method=method, payload=args)

    def get_firewall_schedule(self, **kwargs: dict[str, Any]) -> APIResponse:
        """Read all existing firewall schedules.
        https://github.com/jaredhendrickson13/pfsense-api#3-read-firewall-schedules"""
        url = "/api/v1/firewall/schedule"
        return self.call(url=url, payload=kwargs)

    def update_firewall_schedule(self, **args: dict[str, Any]) -> APIResponse:
        """Update a firewall schedule.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#4-update-schedule"""
        method = "PUT"
        url = "/api/v1/firewall/schedule"
        return self.call(url=url, method=method, payload=args)

    def create_schedule_time_range(self, **args: dict[str, Any]) -> APIResponse:
        """Add a time range to an existing firewall schedule.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-schedule-time-range"""
        method = "POST"
        url = "/api/v1/firewall/schedule/time_range"
        return self.call(url=url, method=method, payload=args)

    def delete_schedule_time_range(self, **args: dict[str, Any]) -> APIResponse:
        """Delete a time range from an existing firewall schedule.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-schedule-time-range"""
        method = "DELETE"
        url = "/api/v1/firewall/schedule/time_range"
        return self.call(url=url, method=method, payload=args)

    def get_firewall_states(self, **kwargs: dict[str, Any]) -> APIResponse:
        """Read the current firewall states. https://github.com/jaredhendrickson13/pfsense-api#1-read-firewall-states"""
        url = "/api/v1/firewall/states"
        return self.call(url=url, payload=kwargs)

    def get_firewall_states_size(self, **kwargs: dict[str, Any]) -> APIResponse:
        """Read the maximum firewall state size, the current firewall state size, and the default firewall state size.
        https://github.com/jaredhendrickson13/pfsense-api#1-read-firewall-state-size"""
        url = "/api/v1/firewall/states/size"
        return self.call(url=url, payload=kwargs)

    def update_firewall_state_size(self, **args: dict[str, Any]) -> APIResponse:
        """Modify the maximum number of firewall state table entries allowed by the system.
        Note: use caution when making this call, setting the maximum state table size to a value lower than
        the current number of firewall state entries WILL choke the system.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-update-firewall-state-size"""
        method = "PUT"
        url = "/api/v1/firewall/states/size"
        return self.call(url=url, method=method, payload=args)

    def create_traffic_shaper(self, **args: dict[str, Any]) -> APIResponse:
        """Add a traffic shaper policy to an interface.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-traffic-shaper"""
        method = "POST"
        url = "/api/v1/firewall/traffic_shaper"
        return self.call(url=url, method=method, payload=args)

    def delete_traffic_shaper(self, **args: dict[str, Any]) -> APIResponse:
        """Delete a traffic shaper policy from an interface.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-traffic-shaper"""
        method = "DELETE"
        url = "/api/v1/firewall/traffic_shaper"
        return self.call(url=url, method=method, payload=args)

    def get_traffic_shaper(self, **kwargs: dict[str, Any]) -> APIResponse:
        """Read all configured traffic shapers.
        https://github.com/jaredhendrickson13/pfsense-api#3-read-traffic-shapers"""
        url = "/api/v1/firewall/traffic_shaper"
        return self.call(url=url, payload=kwargs)

    def update_traffic_shaper(self, **args: dict[str, Any]) -> APIResponse:
        """Update a traffic shaper policy for an interface.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#4-update-traffic-shaper"""
        url = "/api/v1/firewall/traffic_shaper"
        method = "PUT"
        return self.call(url=url, method=method, payload=args)

    def create_traffic_shaper_limiter(self, **args: dict[str, Any]) -> APIResponse:
        """Add a traffic shaper limiter.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-limiter"""
        url = "/api/v1/firewall/traffic_shaper/limiter"
        method = "POST"
        return self.call(url=url, method=method, payload=args)

    def delete_traffic_shaper_limiter(self, **args: dict[str, Any]) -> APIResponse:
        """Delete a traffic shaper limiter.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-limiter"""
        method = "DELETE"
        url = "/api/v1/firewall/traffic_shaper/limiter"
        return self.call(url=url, method=method, payload=args)

    def get_traffic_shaper_limiter(self, **kwargs: dict[str, Any]) -> APIResponse:
        """Get the traffic shaper limiters.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#3-read-limiters"""
        url = "/api/v1/firewall/traffic_shaper/limiter"
        return self.call(url=url, payload=kwargs)

    def create_limiter_bandwidth(self, **args: dict[str, Any]) -> APIResponse:
        """Create a limiter bandwidth setting.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-limiter-bandwidth"""
        method = "POST"
        url = "/api/v1/firewall/traffic_shaper/limiter/bandwidth"
        return self.call(url=url, method=method, payload=args)

    def delete_limiter_bandwidth(self, **args: dict[str, Any]) -> APIResponse:
        """Delete a limiter bandwidth setting.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-limiter-bandwidth"""
        method = "DELETE"
        url = "/api/v1/firewall/traffic_shaper/limiter/bandwidth"
        return self.call(url=url, method=method, payload=args)

    def create_limiter_queue(self, **args: dict[str, Any]) -> APIResponse:
        """Add a child queue to an existing traffic shaper limiter.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-limiter-queue"""
        method = "POST"
        url = "/api/v1/firewall/traffic_shaper/limiter/queue"
        return self.call(url=url, method=method, payload=args)

    def delete_limiter_queue(self, **args: dict[str, Any]) -> APIResponse:
        """Delete a child queue from an existing traffic shaper limiter.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-limiter-queue"""
        method = "DELETE"
        url = "/api/v1/firewall/traffic_shaper/limiter/queue"
        return self.call(url=url, method=method, payload=args)

    def create_firewall_rule(self, **args: dict[str, Any]) -> APIResponse:
        """Create firewall rules. https://github.com/jaredhendrickson13/pfsense-api#3-read-firewall-rules"""
        url = "/api/v1/firewall/rule"
        method = "POST"
        return self.call(url=url, method=method, payload=args)

    @validate_call
    def delete_firewall_rule(self, name: str, apply: bool | None = None) -> APIResponse:
        """Delete firewall rules.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-firewall-rules"""
        url = "/api/v1/firewall/rule"
        method = "DELETE"
        payload: dict[str, str | bool] = {"name": name}
        if apply is not None:
            payload["apply"] = apply
        return self.call(url=url, method=method, payload=payload)

    def update_firewall_rule(self, **args: dict[str, Any]) -> APIResponse:
        """Update firewall rules.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#4-update-firewall-rules"""
        url = "/api/v1/firewall/rule"
        method = "PUT"
        return self.call(url=url, method=method, payload=args)

    def get_firewall_rules(self) -> APIResponse:
        """Read existing firewall rules."""
        url = "/api/v1/firewall/rule"
        return self.call(url=url, method="GET")

    def create_traffic_shaper_queue(self, **args: dict[str, Any]) -> APIResponse:
        """Add a queue to a traffic shaper interface.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-traffic-shaper-queue"""
        method = "POST"
        url = "/api/v1/firewall/traffic_shaper/queue"
        return self.call(url=url, method=method, payload=args)

    def delete_traffic_shaper_queue(self, **args: dict[str, Any]) -> APIResponse:
        """Delete a queue from a traffic shaper interface.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-traffic-shaper-queue"""
        method = "DELETE"
        url = "/api/v1/firewall/traffic_shaper/queue"
        return self.call(url=url, method=method, payload=args)

    def create_virtual_ip(self, **args: dict[str, Any]) -> APIResponse:
        """Add a new virtual IP.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-virtual-ips"""
        method = "POST"
        url = "/api/v1/firewall/virtual_ip"
        return self.call(url=url, method=method, payload=args)

    def delete_virtual_ip(self, **args: dict[str, Any]) -> APIResponse:
        """Delete a virtual IP.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-virtual-ips"""
        method = "DELETE"
        url = "/api/v1/firewall/virtual_ip"
        return self.call(url=url, method=method, payload=args)

    def get_virtual_ip(self, **kwargs: dict[str, Any]) -> APIResponse:
        """Read virtual IP assignments.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#3-read-virtual-ips"""
        return self.call("/api/v1/firewall/virtual_ip", payload=kwargs)

    def update_virtual_ip(self, **args: dict[str, Any]) -> APIResponse:
        """Update a virtual IP.
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#4-update-virtual-ips"""
        method = "PUT"
        url = "/api/v1/firewall/virtual_ip"
        return self.call(url=url, method=method, payload=args)
