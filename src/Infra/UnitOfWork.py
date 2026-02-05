class UnitOfWork():
    def __init__(self, session):
        self.seen = set()
        self.session = session
    def register(self, aggregate):
        self.seen.add(aggregate)

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        
    def collect_events(self):
        events = []
        for aggregate in self.seen:
            events.extend(aggregate.aggregate_root.pull_events())
        return events