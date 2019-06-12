from crashbin_app import signals

@signals.receiver(signals.new_report)
def on_new_report(report, **kwargs):
    print(f"new report: {report.title}")

@signals.receiver(signals.bin_assigned)
def on_bin_assigned(report, old_bin, new_bin, **kwargs):
    print(f"bin assigned: {old_bin} -> {new_bin}")
