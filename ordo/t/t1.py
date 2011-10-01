import yaml
import job


j = job.Job()

j.name="TEST1_YAML"
j.cmd="ls -l /"

jy = yaml.dump(j)

print jy

