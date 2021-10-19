create table if not exists systems (system_name text, star_class text, system_id int unique, x float, y float, z float,
updated_timestamp text, software_name text, software_version text);
create table if not exists routes (route_id int, point_id int, system_id int, timestamp str);
create table if not exists systems_history (old_system_name text, new_system_name text, old_star_class text,
new_star_class text, new_system_id int, old_system_id int, old_x text, new_x text, old_y text, new_y text, old_z text,
new_z text, old_updated_timestamp text, new_updated_timestamp text, software_name text, software_version text,
timestamp text default current_timestamp);
create trigger if not exists update_systems_history_insert
before insert on systems
begin
insert into systems_history (new_system_name, new_star_class, new_system_id, new_x, new_y, new_z, new_updated_timestamp,
software_name, software_version)
values (new.system_name, new.star_class, new.system_id, new.x, new.y, new.z, new.updated_timestamp, new.software_name, new.software_version);
end;
create trigger if not exists update_systems_history_update
before update on systems
begin
insert into systems_history (
old_system_name, new_system_name,
old_star_class, new_star_class,
old_system_id, new_system_id,
old_x, new_x,
old_y, new_y,
old_z, new_z,
old_updated_timestamp, new_updated_timestamp,
software_name,
software_version) values (
old.system_name, new.system_name,
old.star_class, new.star_class,
old.system_id, new.system_id,
old.x, new.x,
old.y, new.y,
old.z, new.z,
old.updated_timestamp, new.updated_timestamp,
new.software_name,
new.software_version);
end;