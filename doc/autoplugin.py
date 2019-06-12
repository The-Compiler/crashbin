from crashbin_app import signals, models

@signals.receiver(signals.new_report)
def on_new_report(report, **kwargs):
    if report.title.endswith('Exception: Forced crash'):
        new_bin = models.Bin.objects.get(name='Forced crashes')
        report.assign_to_bin(new_bin)
