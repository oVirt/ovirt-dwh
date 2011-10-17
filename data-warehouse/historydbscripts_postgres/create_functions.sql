----------------------------------
-- 		create functions		--
----------------------------------



CREATE OR REPLACE FUNCTION GetPathInNames(tagHistoryID int)
RETURNS VARCHAR(4000)
   AS $function$
   DECLARE
   v_id  UUID;
   v_path_names  VARCHAR(4000);
   SWV_path VARCHAR(4000);
BEGIN
   SELECT tag_path into SWV_path FROM tag_details WHERE history_id = tagHistoryID;
   v_path_names := '/root';
   IF (SWV_path IS NULL or SWV_path = '') THEN
	RETURN SWV_path;
   ELSEIF (SWV_path = '/00000000-0000-0000-0000-000000000000') THEN
	RETURN v_path_names;
   ELSE 
      SWV_path := SUBSTR(SWV_path,38);
      WHILE (LENGTH(SWV_path) > 0) LOOP
         v_id := cast(SUBSTR(SWV_path,2,36) as UUID);
         SWV_path := SUBSTR(SWV_path,38);
         SELECT  v_path_names || '/' || tag_name INTO v_path_names FROM tag_details where tag_id = v_id;
      END LOOP;
   end if;
   RETURN v_path_names;
END; $function$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION GetPathIDs(currentTagID UUID, runNumber int default 0)
RETURNS VARCHAR(4000)
   AS $function$
   DECLARE 
	ParentID UUID;
BEGIN
   IF currentTagID IS NULL then
      RETURN NULL;
   end if;
   select parent_id INTO ParentID FROM tag_relations_history WHERE entity_id = currentTagID and history_id in  (SELECT max(a.history_id) 
														FROM tag_relations_history a
														WHERE a.entity_id = currentTagID);
	IF runNumber = 0 then
		RETURN coalesce(GetPathIDs(ParentID, runNumber + 1),'/');
	ELSE
		RETURN coalesce(GetPathIDs(ParentID, runNumber + 1) || '/' ,'/') || currentTagID;
   end if;
END; $function$
LANGUAGE plpgsql;

Create or replace FUNCTION update_tags_path_child(thisUpdate TIMESTAMP WITH TIME ZONE)
RETURNS VOID AS $procedure$
BEGIN
	/*This inserts all children of the changed nodes with their new path*/
	Insert into  tag_details(tag_id,
				  tag_name,
				  tag_description,
				  tag_path,
				  tag_level,
				  create_date,
				  update_date)
	select distinct a.tag_id,
			a.tag_name,
			a.tag_description,
			c.new_child_path || SUBSTR(a.tag_path,LENGTH(b.old_child_path) + 1),
			LENGTH(c.new_child_path || SUBSTR(a.tag_path,LENGTH(b.old_child_path) + 1)) - LENGTH(REPLACE((c.new_child_path || SUBSTR(a.tag_path,LENGTH(b.old_child_path) + 1)),'/','')),
			a.create_date,
			thisUpdate
	FROM tag_details a,
	     (select e.tag_path || '/' || CAST(e.tag_id AS VARCHAR(36)) as old_child_path, e.tag_id as parent /*36 is the uuid length*/
	      from tag_details e
	      where e.history_id = (SELECT max(f.history_id)
				    FROM tag_details f
			   	    WHERE (f.update_date < thisUpdate or f.update_date IS NULL) 
						   AND f.tag_id = e.tag_id)
		   AND e.delete_date IS NULL) b,
	     (select tag_path || '/' || CAST(tag_id AS VARCHAR(36)) as new_child_path, tag_id as parent /*36 is the uuid length*/
	      from tag_details
	      where update_date = thisUpdate
		    and delete_date IS NULL) c
	Where a.tag_path like b.old_child_path || '%' and
	      b.parent = c.parent and
	      not exists (SELECT z.tag_id, z.tag_path FROM tag_details as z WHERE tag_id = a.tag_id and z.tag_path = c.new_child_path || SUBSTR(a.tag_path,LENGTH(b.old_child_path) + 1));
	RETURN;
END; $procedure$
LANGUAGE plpgsql;

