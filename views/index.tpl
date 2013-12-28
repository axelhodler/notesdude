% rebase layout

% include navbar user=user

<div class="container">
  <div class="row">
    <div class="col-md-8">
% include noteslist rows=rows, user=user
    </div>
    <div class="col-md-4">
% include panel_to_add_note user=user, fail=fail
    </div>
  </div>
</div>
