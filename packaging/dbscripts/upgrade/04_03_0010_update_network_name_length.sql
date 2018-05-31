-- Update host_interface_configuration table network_name filed length to 256

ALTER TABLE host_interface_configuration ALTER COLUMN logical_network_name TYPE varchar(256);

-- Update vm_interface_configuration table network_name filed length to 256

ALTER TABLE vm_interface_configuration ALTER COLUMN logical_network_name TYPE varchar(256);
