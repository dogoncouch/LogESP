# Asset Management Documentation

- [Organizational Units](#organizational-units)
- [Hardware Assets](#hardware-assets)
- [Software Assets](#software-assets)

## Organizational Units
Organizational units can be departments, office locations, or anything else by which your organization can be ... organized. OUs can have a parent OU; an organization should be arranged in a tree.

## Hardware Assets
Hardware assets can be any piece of hardware, from door locks to servers to USB thumb drives. Each hardware asset belongs to an OU. Hardware assets can have a parent hardware asset (for example, a hard drive in a server), along with the following attributes:

- `name` - the asset name
- `desc` - a description of the asset
- `asset_owner` - the person responsible for the asset
- `asset_custodian` - the custodian of the asset
- `hardware_type` - the hardware type
- `device_maker` - the manufacturer
- `device_model` - the device model
- `property_id` - the asset's company-assigned property ID
- `location` - the location of the asset
- `status` - the status of the asset
- `date_added` - the date the asset was added
- `date_eol` - the asset's end of life date

## Software Assets
Software assets can be anything from files to operating systems. Software assets belong to an OU, and can have multiple parent hardware and software assets (for example, a virtual machine that runs on a cluster of 20 servers). They also have the following attributes:

- `custodian_swam` - Software asset management custodian
- `custodian_csm` - configuration management custodian
- `custodian_vul` - patching/vulnerability management custodian
- `software_type` - the software type
- `package_vendor` - the package vendor
- `package_name` - the package name
- `package_version` - the package version
- `sw_property_id` - the asset's company-assigned property ID
- `status` - the status of the asset
- `date_added` - the date the asset was added
- `date_eol` - the asset's end of life date
- `hostname` - the host name, if applicable
- `domain_name` - the domain name
- `ip4_address_1` - an IPv4 address
- `ip4_address_2` - an IPv4 address
- `ip4_address_3` - an IPv4 address
- `ip4_address_4` - an IPv4 address
- `ip4_address_5` - an IPv4 address
- `ip4_address_6` - an IPv4 address
- `ip4_address_7` - an IPv4 address
- `ip4_address_8` - an IPv4 address
- `ip6_address_5` - an IPv6 address
- `ip6_address_6` - an IPv6 address
- `ip6_address_7` - an IPv6 address
- `ip6_address_8` - an IPv6 address
- `ip6_address_1` - an IPv6 address
- `ip6_address_2` - an IPv6 address
- `ip6_address_3` - an IPv6 address
- `ip6_address_4` - an IPv6 address
