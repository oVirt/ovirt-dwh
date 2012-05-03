CREATE SEQUENCE disk_vm_device_history_seq INCREMENT BY 1 START WITH 1;
CREATE TABLE vm_device_history
(
  history_id INTEGER DEFAULT NEXTVAL('disk_vm_device_history_seq') PRIMARY KEY NOT NULL,
  vm_id uuid NOT NULL,
  device_id uuid NOT NULL,
  type character varying(30) NOT NULL,
  address character varying(255) NOT NULL,
  is_managed boolean NOT NULL DEFAULT false,
  is_plugged boolean,
  is_readonly boolean NOT NULL DEFAULT false,
  vm_configuration_version INTEGER,
  device_configuration_version INTEGER,
  create_date TIMESTAMP WITH TIME ZONE NOT NULL,
  update_date TIMESTAMP WITH TIME ZONE,
  delete_date TIMESTAMP WITH TIME ZONE
) WITH OIDS;

CREATE INDEX IDX_vm_device_history_vm_id_type ON vm_device_history (vm_id, type);
