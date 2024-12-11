from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from sqlalchemy import func

db = SQLAlchemy()

class Rate(db.Model):
    """Model that represents a single data of exchange rate."""
    date = db.Column(db.Date, primary_key=True)
    rate = db.Column(db.Float, nullable=False)
    is_lowest = db.Column(db.Boolean, default=False, nullable=False)

    @staticmethod
    def add_rate(date, rate):
        try:
            # Check if the rate for the given date exists
            existing_rate = Rate.query.filter_by(date=date).first()
            if existing_rate:
                # Update the rate and reset 'is_lowest' flag
                existing_rate.rate = rate
                existing_rate.is_lowest = False
            else:
                # Add a new rate record
                new_rate = Rate(date=date, rate=rate, is_lowest=False)
                db.session.add(new_rate)
            
            db.session.commit()

            # Only keep the latest 30 rate records
            if db.session.query(Rate).count() > 30:
                oldest_rate = Rate.query.order_by(Rate.date).first()
                if oldest_rate:
                    db.session.delete(oldest_rate)
                    db.session.commit()

            return existing_rate if existing_rate else new_rate
        except Exception as e:
            print(f"Database error: {e}")
            db.session.rollback()
            raise

    
    # @staticmethod
    # def is_weekly_lowest_rate(d):
    #     curr_data = Rate.query.get_or_404(d)
    #     pre_lowest_data = Rate.query.filter_by(is_lowest=True).first()
    #     if pre_lowest_data:
    #         if curr_data.rate < pre_lowest_data.rate:
    #             curr_data.is_lowest = True
    #             pre_lowest_data.is_lowest = False
    #             db.session.commit()
    #             return True
    #     else:
    #         rate_data = Rate.query.filter(Rate.date < d and Rate.date > d - 7).all()
    #         for rd in rate_data:
    #             if rd.rate < curr_data.rate:
    #                 return False
    #         curr_data.is_lowest = True
    #         pre_lowest_data.is_lowest = False
    #         db.session.commit()  
    #         return True
    
    # @staticmethod
    # def is_monthly_lowest_rate(d):
    #     curr_rate = Rate.query.filter_by(date=d).first().rate
    #     lowest_rate
    #     for rd in rate_data:
    #         if rd.rate < curr_rate:
    #             return False    
    #     return True