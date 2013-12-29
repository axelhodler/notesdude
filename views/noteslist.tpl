<h1>Notes</h1>
<table class="table">
  <tr>
    <th class="col-md-3">Title</th>
    <th class="col-md-5">Content</th>
    <th></th>
  </tr>
  %for row in rows:
  <tr>
    <td>{{row.get('title')}}</td>
    <td>{{row.get('content')}}</td>
    <td><form action="/delete/{{row.get('id')}}">
      %if user_is_logged_in:
      <input class="btn btn-danger btn-xs pull-right" type="submit" value="Delete Note">
      %else:
      <input class="btn btn-danger btn-xs pull-right" type="submit" value="Delete Note" disabled="disabled">
      %end
    </form>
    </td>
  </tr>
  %end
</table>
