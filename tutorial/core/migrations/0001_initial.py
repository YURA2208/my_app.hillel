from django.db import migrations, models


class Migration(migrations.Migration):

   initial = True

   dependencies = [
   ]

   operations = [
       migrations.CreateModel(
           name='Actor',
           fields=[
               ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
               ('name', models.CharField(max_length=100)),
               ('birthday', models.DateField()),
               ('die', models.DateField(blank=True, null=True)),
           ],
           options={
               'ordering': ['name'],
           },
       ),
       migrations.CreateModel(
           name='Movie',
           fields=[
               ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
               ('title', models.CharField(max_length=100)),
               ('plot', models.TextField()),
               ('year', models.PositiveIntegerField()),
               ('rating', models.IntegerField(
                   choices=[(0, 'NR - Not Rated'), (1, 'G - General Audiences'), (2, 'PG - Parental Guidance'),
                            (3, 'R - Restricted')], default=0)),
               ('runtime', models.PositiveIntegerField()),
               ('actors', models.ManyToManyField()),
           ],
           options={
               'ordering': ['-year', 'title'],
           },
       ),
   ]