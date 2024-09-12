from app.models import RekonData, Sfd, Indicator, Criteria
from app.controllers.utils import calculate_indicator_mark  # Supposons que cette fonction existe

async def rekonData_create(
    rekon_data_list: list[dict],
    sfd: Sfd,
    year: int = 2024,
) -> list[RekonData]:
    """Create RekonData entries and create or update associated Indicators."""
    created_rekon_data = []
    indicators_to_update = {}

    for data in rekon_data_list:
        # Check if the indicator exists, if not create it
        indicator = await Indicator.get(data['indicator'])
        if not indicator:
            criteria = await Criteria.get_or_404(data['criteria'])
            indicator = await Indicator(
                sfd=sfd,
                criteria=criteria,
                name=data['indicator_name'],
                year=year
            ).create()
            data['indicator'] = indicator

        # Create RekonData
        rekon_data = await RekonData(
            sfd=sfd,
            account_number=data['account_number'],
            amount=data['amount'],
            year=year,
            indicator=data['indicator'],
            criteria=data['criteria']
        ).create()
        created_rekon_data.append(rekon_data)

        # Group RekonData by indicator for later calculation
        if data['indicator'] not in indicators_to_update:
            indicators_to_update[data['indicator']] = []
        indicators_to_update[data['indicator']].append(rekon_data)

    # create or updateIndicators
    for indicator, rekon_data_list in indicators_to_update.items():
        indicator = await Indicator.get(indicator)
        if not indicator:
            # If indicator doesn't exist, create it
            criteria = await Criteria.get(data['criteria'])  # Assuming criteria is provided
            indicator = await Indicator(
                sfd=sfd,
                criteria=criteria,
                name=data['indicator_name'],  # Assuming indicator_name is provided
                year=year
            ).create()

        # Calculate indicator mark
        calculated_mark = calculate_indicator_mark(rekon_data_list)

        # Update indicator
        indicator.mark = calculated_mark
        await indicator.save()

    return created_rekon_data
